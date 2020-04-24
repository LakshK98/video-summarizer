import numpy as np
import os
import math
import time
import google_stt
import preprocess_text
import ann_summarize
import video_segmentation
import drop_and_forward


# import ann_summarize

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def normalize(v):
    return (v-min(v))/(max(v)-min(v))

def get_sentence_scores(transcript_timestamp_dict):
    transcripts = list(transcript_timestamp_dict.keys())
    cleaned_lines = preprocess_text.clean_lines([lines for lines in transcripts])
    word_embeddings = preprocess_text.load_word_embeddings()
    sentence_vectors = preprocess_text.get_sentence_vectors(word_embeddings, cleaned_lines)
    sentence_scores = ann_summarize.get_summary(sentence_vectors, False)
    # return softmax(sentence_scores)
    # print("sen_sc",sentence_scores)
    # print("normalize_sens_sc",normalize(sentence_scores))
    # print("softmax_norm_sen_sc",softmax(normalize(sentence_scores)))
    return softmax(normalize(sentence_scores))


def create_shots(transcript_timestamp_dict,boundaries,orb_ratios,sentence_scores):
    shots = []
    # If there is no spoken content
    if(len(sentence_scores)==0):
        for i in range(len(boundaries)-1):
            shot_info = {}
            shot_info['start']=boundaries[i]
            shot_info['end']=boundaries[i+1]

            shot_info['spoken_start'] = boundaries[i]
            shot_info['spoken_end'] = boundaries[i]

            shot_info['spoken_score'] = 0

            silent_orb_ratios = orb_ratios[math.ceil(shot_info['start']):math.floor(shot_info['end'])]

            shot_info['silent_score'] = np.mean(silent_orb_ratios)
            # if something is not equal to itself it is nan
            # this stement gives 0 if val is nan
            shot_info['silent_score'] = shot_info['silent_score'] if shot_info['silent_score'] == shot_info[
                'silent_score'] else 0

            shots.append(shot_info)
        new_silent_scores = softmax([x['silent_score'] for x in shots])

        for i, shot in enumerate(shots):
            shot['silent_score'] = new_silent_scores[i]
            shot['spoken_len'] = 0
            shot['silent_len'] = shot['end'] - shot['start']
        return shots

    transcripts = list(transcript_timestamp_dict.keys())
    for i in range(len(transcripts)):
        start, end = transcript_timestamp_dict[transcripts[i]]
        shot_info = {}

        shot_info['spoken_start'] = start
        shot_info['spoken_end'] = end

        shot_info['start'] = 0 if i == 0 else shots[-1]['end']



        # end can be 148.6 but boundaries will go to 148 because int() taken when calculating total_seconds
        try :
            shot_info['end'] = boundaries[list(map(lambda itr: itr > end, boundaries)).index(True)]
        except ValueError as v:
            shot_info['end']=boundaries[-1]

        shot_info['end'] = shot_info['end'] if i == len(transcripts) - 1 else min(shot_info['end'],
                                                                                  transcript_timestamp_dict[
                                                                                      transcripts[i + 1]][0])

        shot_info['spoken_score'] = sentence_scores[i]



        # uncomment this if u want silent score to be calculated as the mean of orb ratios only from the silent part
        # silent_orb_ratios = orb_ratios[math.ceil(shot_info['start']):math.floor(shot_info['spoken_start'])]
        # silent_orb_ratios += orb_ratios[math.ceil(shot_info['spoken_end']):math.floor(shot_info['end'])]
        # silent_orb_ratios = np.array(silent_orb_ratios)

        silent_orb_ratios=orb_ratios[math.ceil(shot_info['start']):math.floor(shot_info['end'])]

        shot_info['silent_score'] = np.mean(silent_orb_ratios)
        # if something is not equal to itself it is nan
        # this stement gives 0 if val is nan
        shot_info['silent_score'] = shot_info['silent_score'] if shot_info['silent_score'] == shot_info[
            'silent_score'] else 0

        shots.append(shot_info)

    new_silent_scores = softmax([x['silent_score'] for x in shots])

    for i, shot in enumerate(shots):
        shot['silent_score'] = new_silent_scores[i]
        shot['spoken_len'] = shot['spoken_end'] - shot['spoken_start']
        shot['silent_len'] = shot['end'] - shot['start'] - shot['spoken_len']

    return shots

def add_video_cut_ffmpeg(start ,end ,speedup,index):
    if start != end:
        video_command="[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(start,end,speedup, index)
        audio_command="[0:a]atrim={}:{},atempo={}[a{}]; ".format(start,end,speedup, index)
        return video_command+audio_command,index+1
    return "",index
def write_summarized_video(video_filepath,shots,selected_shot_indices,spoken_speed,silent_speed):
    index = 0
    ffmpeg_command = "ffmpeg -i " +video_filepath+ " -filter_complex \""
    for i, shot in enumerate(shots):
        print(shot)

        if i in selected_shot_indices:
            add_command,index=add_video_cut_ffmpeg(shot['start'],shot['spoken_start'],silent_speed,index)
            ffmpeg_command +=add_command


            # ffmpeg_command += "[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['start'],
            #                                                                                     shot['spoken_start'],
            #                                                                                     silent_speed, index)
            # ffmpeg_command += "[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['start'], shot['spoken_start'],
            #                                                              silent_speed, index)

            add_command, index =add_video_cut_ffmpeg(shot['spoken_start'],shot['spoken_end'],spoken_speed,index)
            ffmpeg_command += add_command
            # ffmpeg_command += "[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['spoken_start'],
            #                                                                                     shot['spoken_end'],
            #                                                                                     spoken_speed, index)
            # ffmpeg_command += "[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['spoken_start'], shot['spoken_end'],
            #                                                              spoken_speed, index)

            add_command, index =add_video_cut_ffmpeg(shot['spoken_end'],shot['end'],silent_speed,index)
            ffmpeg_command += add_command
            # ffmpeg_command += "[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['spoken_end'],
            #                                                                                     shot['end'],
            #                                                                                     silent_speed, index)
            # ffmpeg_command += "[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['spoken_end'], shot['end'], silent_speed,
            #                                                              index)

    for i in range(index):
        ffmpeg_command += "[v{}][a{}]".format(i, i)
    ffmpeg_command += "concat=n={}:v=1:a=1[outv][outa]\"  -map \"[outv]\" -map \"[outa]\" summarized_videos/{}".format(index,os.path.basename(video_filepath))

    print(ffmpeg_command)

    os.system(ffmpeg_command)

def summarize(file_path,compression_ratio):
    time_start=time.time()
    transcript_timestamp_dict = google_stt.get_transcript(file_path)
    print("transcript time:",time.time()-time_start)
    time_start=time.time()
    print()
    print()
    print()

    print(transcript_timestamp_dict)

    sentence_scores=get_sentence_scores(transcript_timestamp_dict)
    print("sentence score time:", time.time() - time_start)
    time_start = time.time()
    print()
    print()
    print()

    orb_ratios,total_seconds=video_segmentation.get_orb_ratios(file_path)

    print("orb ratios:", time.time() - time_start)
    time_start = time.time()
    print()
    print()
    print()
    boundaries=video_segmentation.get_boundaries(orb_ratios,total_seconds)
    print("orb boundaries:", time.time() - time_start)
    time_start = time.time()
    print()
    print()
    print()


    shots=create_shots(transcript_timestamp_dict,boundaries,orb_ratios,sentence_scores)


    selected_shots, selected_spoken_speed, selected_silent_speed=drop_and_forward.drop_and_forward_algo(total_seconds,compression_ratio,shots)
    print("cut forward algo:", time.time() - time_start)
    time_start = time.time()
    print()
    print()
    print()
    write_summarized_video(file_path,shots,selected_shots,selected_spoken_speed,selected_silent_speed)
    print("write:", time.time() - time_start)
    time_start = time.time()
    print()
    print()
    print()
# summarize("videos/xwqBXPGE9pQ.mp4",0.3)

