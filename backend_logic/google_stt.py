
# Import libraries
from pydub import AudioSegment
import os
import time
import pickle
bucket_name = "stt_bucket_ly" #Name of the bucket created in the step before

# import io
# import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage
from google.oauth2 import service_account

#
# # Convert Video to Audio
# import moviepy.editor as mp
import glob

# video_paths=glob.glob("/Users/lakshkotian/Documents/ly/textrank_test/tvsum/*.mp4")
# print(video_paths)
# os.path.basename(img_path)
# for video_path in video_paths:
#     clip = mp.VideoFileClip(video_path)
#     try:
#         os.mkdir("/Users/lakshkotian/Documents/ly/textrank_test/tvsum/"+os.path.basename(video_path)[:-4])
#     except e:
#         print("exists")
#     clip.audio.write_audiofile("/Users/lakshkotian/Documents/ly/textrank_test/tvsum/"+os.path.basename(video_path)[:-4]+".mp3")



def video_to_audio(filepath,audio_path):
    sound = AudioSegment.from_file(filepath, format="mp4")
    sound = sound.set_channels(1)
    sound.export(audio_path, format="wav")
    return sound

def get_frame_rate(sound):
    return sound.frame_rate


def upload_blob(source_file_path, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json('gcp cred/ly-stt-1582263496331-f723d8a35a04.json')
    bucket = storage_client.get_bucket(bucket_name)
    bucket_has_audio = storage.Blob(bucket=bucket, name=destination_blob_name).exists(storage_client)
    if not bucket_has_audio:
        blob = bucket.blob(destination_blob_name)

        blob._chunk_size = 4194304

        blob.upload_from_filename(source_file_path)

    print(bucket_has_audio)
    print("done")
    # print(bucket)
    # blob = bucket.blob(destination_blob_name)
    # print(blob)
    # blob.upload_from_filename(source_file_path)
#     blob.upload_from_string('V')

#



def google_transcribe( audio_name,frame_rate):
    gcs_uri = 'gs://' + bucket_name + '/' + audio_name
    transcript = ''
    credentials = service_account.Credentials.from_service_account_file('gcp cred/ly-stt-1582263496331-f723d8a35a04.json')

    client = speech.SpeechClient(credentials=credentials)
    audio = types.RecognitionAudio(uri=gcs_uri)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code='en-US',
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)

    #     for result in response.results:
    #         transcript += result.alternatives[0].transcript

    #     delete_blob(bucket_name, destination_blob_name)
    transcript_with_timestamp =response.results
    transcript_timestamp_dict = {}
    for result in transcript_with_timestamp:
        alternative = result.alternatives[0]
        print(alternative.transcript)
        start_time = alternative.words[0].start_time
        end_time = alternative.words[-1].end_time
        transcript_timestamp_dict[alternative.transcript] = [start_time.seconds + start_time.nanos * 1e-9,
                                                             end_time.seconds + end_time.nanos * 1e-9]
    return transcript_timestamp_dict

def get_trascript_from_pickle(pickle_name):
    pickle_in = open("test_transcript_picles/"+pickle_name, "rb")
    transcript_timestamp_dict = pickle.load(pickle_in)
    return transcript_timestamp_dict

def get_transcript(filepath):


    audio_name=os.path.basename(filepath)[:-4]+'.wav'
    audio_path=os.path.join(os.getcwd(),'audios',audio_name)



    print(audio_path)



    sound=video_to_audio(filepath,audio_path)
    frame_rate=get_frame_rate(sound)

    time_start=time.time()
    upload_blob(audio_path,audio_name)

    transcript_timestamp_dict=google_transcribe(audio_name,frame_rate)
    pickle_out = open("test_transcript_picles/" + audio_name[:-4] + ".pickle", "wb")
    pickle.dump(transcript_timestamp_dict, pickle_out)
    pickle_out.close()

    # transcript_timestamp_dict=get_trascript_from_pickle("akI8YFjEmUw.pickle")

    print(time.time()-time_start)
    return transcript_timestamp_dict



# get_transcript('videos/akI8YFjEmUw.mp4')
