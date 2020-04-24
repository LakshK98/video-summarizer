
import pickle
# from moviepy.editor import *
# import moviepy.video.fx.all as vfx

import os

shots=[{'spoken_start': 6.7, 'spoken_end': 25.2, 'start': 0, 'end': 26, 'spoken_score': 0.19999643, 'silent_score': 0.21926726152171136, 'spoken_len': 18.5, 'silent_len': 7.5},
{'spoken_start': 26.5, 'spoken_end': 46.0, 'start': 26, 'end': 47.0, 'spoken_score': 0.19999643, 'silent_score': 0.1884672424200621, 'spoken_len': 19.5, 'silent_len': 1.5},
{'spoken_start': 47.0, 'spoken_end': 86.9, 'start': 47.0, 'end': 87, 'spoken_score': 0.20001426, 'silent_score': 0.20312997346670436, 'spoken_len': 39.900000000000006, 'silent_len': 0.09999999999999432},
{'spoken_start': 88.1, 'spoken_end': 118.5, 'start': 87, 'end': 119.5, 'spoken_score': 0.19999643, 'silent_score': 0.2047561970178872, 'spoken_len': 30.400000000000006, 'silent_len': 2.0999999999999943},
{'spoken_start': 119.5, 'spoken_end': 130.9, 'start': 119.5, 'end': 133, 'spoken_score': 0.19999643, 'silent_score': 0.184379325573635, 'spoken_len': 11.400000000000006, 'silent_len': 2.0999999999999943}]
subclips = []
shot_indices=[4, 1, 0]
shots.sort(key=lambda s:s['start'])


# PTS-STARTPTS specifies start from 0
# PTS/3 says 1/3rd the number of pts to be used so it will skip frames
# atempo increases speed of audio


index=0
spoken_speed=1
silent_speed=3
ffmpeg_command="ffmpeg -i videos/akI8YFjEmUw.mp4 -filter_complex \""
for i,shot in enumerate(shots):
    print(shot)

    if i in shot_indices:

        ffmpeg_command+="[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['start'] , shot['spoken_start'],silent_speed,index)
        ffmpeg_command+="[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['start'] , shot['spoken_start'],silent_speed,index)
        index+=1

        ffmpeg_command+="[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['spoken_start'] , shot['spoken_end'],spoken_speed,index)
        ffmpeg_command+="[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['spoken_start'] , shot['spoken_end'],spoken_speed,index)
        index += 1

        ffmpeg_command+="[0:v]trim={}:{},setpts=PTS-STARTPTS,setpts=PTS/{}[v{}]; ".format(shot['spoken_end'] , shot['end'],silent_speed,index)
        ffmpeg_command+="[0:a]atrim={}:{},atempo={}[a{}]; ".format(shot['spoken_end'] , shot['end'],silent_speed,index)
        index += 1


for i in range(index):
    ffmpeg_command+="[v{}][a{}]".format(i,i)
ffmpeg_command+="concat=n={}:v=1:a=1[outv][outa]\"  -map \"[outv]\" -map \"[outa]\" axxxx.mp4".format(index)

print (ffmpeg_command)

os.system(ffmpeg_command)

# ffmpeg -i /Users/lakshkotian/Documents/ly_final/vsum/data/videos/4wU_LUjG5Ic.mp4 -filter_complex "[0:v]trim=32:32.1,setpts=PTS/3[v0]; [0:a]atrim=32:32.1,atempo=3[a0]; \[0:v]trim=32.1:44.8,setpts=PTS/1[v1]; \[0:a]atrim=32.1:44.8,atempo=1[a1]; \[0:v]trim=44.8:48,setpts=PTS/3[v2]; \[0:a]atrim=44.8:48,atempo=3[a2]; \[0:v]trim=48:62.6,setpts=PTS/3[v3]; \[0:a]atrim=48:62.6,atempo=3[a3]; \[0:v]trim=62.6:64.3,setpts=PTS/1[v4]; \[0:a]atrim=62.6:64.3,atempo=1[a4]; \[0:v]trim=64.3:74,setpts=PTS/3[v5]; \[0:a]atrim=64.3:74,atempo=3[a5]; \[0:v]trim=74:74.4,setpts=PTS/3[v6]; \[0:a]atrim=74:74.4,atempo=3[a6]; \[0:v]trim=74.4:88.7,setpts=PTS/1[v7]; \[0:a]atrim=74.4:88.7,atempo=1[a7]; \[0:v]trim=88.7:89,setpts=PTS/3[v8]; \[0:a]atrim=88.7:89,atempo=3[a8]; \[0:v]trim=121:125.3,setpts=PTS/3[v9]; \[0:a]atrim=121:125.3,atempo=3[a9]; \[0:v]trim=125.3:131.7,setpts=PTS/1[v10]; \[0:a]atrim=125.3:131.7,atempo=1[a10]; \[0:v]trim=131.7:134,setpts=PTS/3[v11]; \[0:a]atrim=131.7:134,atempo=3[a11]; \[v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12]concat=n=2:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" pyffmpeg.mp4


# ffmpeg -i /Users/lakshkotian/Documents/ly_final/vsum/data/videos/4wU_LUjG5Ic.mp4 -filter_complex "[0:v]trim=32:32.1,setpts=PTS/3[v0]; [0:a]atrim=32:32.1,atempo=3[a0]; [0:v]trim=32.1:44.8,setpts=PTS/1[v1]; [0:a]atrim=32.1:44.8,atempo=1[a1]; [0:v]trim=44.8:48,setpts=PTS/3[v2]; [0:a]atrim=44.8:48,atempo=3[a2]; [0:v]trim=48:62.6,setpts=PTS/3[v3]; [0:a]atrim=48:62.6,atempo=3[a3]; [0:v]trim=62.6:64.3,setpts=PTS/1[v4]; [0:a]atrim=62.6:64.3,atempo=1[a4]; [0:v]trim=64.3:74,setpts=PTS/3[v5]; [0:a]atrim=64.3:74,atempo=3[a5]; [0:v]trim=74:74.4,setpts=PTS/3[v6]; [0:a]atrim=74:74.4,atempo=3[a6]; [0:v]trim=74.4:88.7,setpts=PTS/1[v7]; [0:a]atrim=74.4:88.7,atempo=1[a7]; [0:v]trim=88.7:89,setpts=PTS/3[v8]; [0:a]atrim=88.7:89,atempo=3[a8]; [0:v]trim=121:125.3,setpts=PTS/3[v9]; [0:a]atrim=121:125.3,atempo=3[a9]; [0:v]trim=125.3:131.7,setpts=PTS/1[v10]; [0:a]atrim=125.3:131.7,atempo=1[a10]; [0:v]trim=131.7:134,setpts=PTS/3[v11]; [0:a]atrim=131.7:134,atempo=3[a11]; [v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12][v12][a12]concat=n=12:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" pyffmpeg.mp4

# ffmpeg -i /Users/lakshkotian/Documents/ly_final/vsum/data/videos/4wU_LUjG5Ic.mp4 -filter_complex "[0:v]trim=32:32.1,setpts=PTS/3[v0]; [0:a]atrim=32:32.1,atempo=3[a0]; [0:v]trim=32.1:44.8,setpts=PTS/1[v1]; [0:a]atrim=32.1:44.8,atempo=1[a1]; [0:v]trim=44.8:48,setpts=PTS/3[v2]; [0:a]atrim=44.8:48,atempo=3[a2]; [0:v]trim=48:62.6,setpts=PTS/3[v3]; [0:a]atrim=48:62.6,atempo=3[a3]; [0:v]trim=62.6:64.3,setpts=PTS/1[v4]; [0:a]atrim=62.6:64.3,atempo=1[a4]; [0:v]trim=64.3:74,setpts=PTS/3[v5]; [0:a]atrim=64.3:74,atempo=3[a5]; [0:v]trim=74:74.4,setpts=PTS/3[v6]; [0:a]atrim=74:74.4,atempo=3[a6]; [0:v]trim=74.4:88.7,setpts=PTS/1[v7]; [0:a]atrim=74.4:88.7,atempo=1[a7]; [0:v]trim=88.7:89,setpts=PTS/3[v8]; [0:a]atrim=88.7:89,atempo=3[a8]; [0:v]trim=121:125.3,setpts=PTS/3[v9]; [0:a]atrim=121:125.3,atempo=3[a9]; [0:v]trim=125.3:131.7,setpts=PTS/1[v10]; [0:a]atrim=125.3:131.7,atempo=1[a10]; [0:v]trim=131.7:134,setpts=PTS/3[v11]; [0:a]atrim=131.7:134,atempo=3[a11]; [v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5][v6][a6][v7][a7][v8][a8][v9][a9][v10][a10][v11][a11]concat=n=12:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" pyffmpeg.mp4

# ffmpeg -i /Users/lakshkotian/Documents/ly_final/vsum/data/videos/4wU_LUjG5Ic.mp4 -filter_complex "[0:v]trim=26:32,setpts=PTS/3[v0]; [0:a]atrim=26:32,atempo=3[a0]; [0:v]trim=32:45,setpts=PTS/1[v1]; [0:a]atrim=32:45,atempo=1[a1]; [0:v]trim=45:48,setpts=PTS/3[v2]; [0:a]atrim=45:48,atempo=3[a2]; [v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" pyffmpeg2.mp4

# ffmpeg -i /Users/lakshkotian/Documents/ly_final/vsum/data/videos/4wU_LUjG5Ic.mp4 -filter_complex "[0:v]trim=26:32,setpts=PTS-STARTPTS,setpts=PTS/3[v0]; [0:a]atrim=26:32,atempo=2[a0];  [v0][a0]concat=n=1:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" pyffmpeg2.mp4


# ffmpeg -i videos/akI8YFjEmUw.mp4 -filter_complex "[0:v]trim=0:6.7,setpts=PTS-STARTPTS,setpts=PTS/3[v0]; [0:a]atrim=0:6.7,atempo=3[a0];" \
#                                                  "[0:v]trim=6.7:25.2,setpts=PTS-STARTPTS,setpts=PTS/1[v1]; [0:a]atrim=6.7:25.2,atempo=1[a1];" \
#                                                  "[0:v]trim=25.2:26,setpts=PTS-STARTPTS,setpts=PTS/3[v2]; [0:a]atrim=25.2:26,atempo=3[a2]; " \
#                                                  "[0:v]trim=26:26.5,setpts=PTS-STARTPTS,setpts=PTS/3[v3]; [0:a]atrim=26:26.5,atempo=3[a3]; " \
#                                                  "[0:v]trim=26.5:46.0,setpts=PTS-STARTPTS,setpts=PTS/1[v4]; [0:a]atrim=26.5:46.0,atempo=1[a4]; " \
#                                                  "[0:v]trim=46.0:47.0,setpts=PTS-STARTPTS,setpts=PTS/3[v5]; [0:a]atrim=46.0:47.0,atempo=3[a5]; " \
#                                                  "[0:v]trim=119.5:119.5,setpts=PTS-STARTPTS,setpts=PTS/3[v6]; [0:a]atrim=119.5:119.5,atempo=3[a6]; " \
#                                                  "[0:v]trim=119.5:130.9,setpts=PTS-STARTPTS,setpts=PTS/1[v7]; [0:a]atrim=119.5:130.9,atempo=1[a7]; " \
#                                                  "[0:v]trim=130.9:133,setpts=PTS-STARTPTS,setpts=PTS/3[v8]; [0:a]atrim=130.9:133,atempo=3[a8]; " \
#                                                  "[v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5][v6][a6][v7][a7][v8][a8]concat=n=9:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" axxxx.mp4
#
# ffmpeg -i videos/akI8YFjEmUw.mp4 -filter_complex "[0:v]trim=0:6.7,setpts=PTS-STARTPTS,setpts=PTS/3[v0]; [0:a]atrim=0:6.7,atempo=3[a0];" \
#                                                  "[0:v]trim=6.7:25.2,setpts=PTS-STARTPTS,setpts=PTS/1[v1]; [0:a]atrim=6.7:25.2,atempo=1[a1];" \
#                                                  "[0:v]trim=25.2:26,setpts=PTS-STARTPTS,setpts=PTS/3[v2]; [0:a]atrim=25.2:26,atempo=3[a2]; " \
#                                                  "[v0][a0][v1][a1][v2][a2] concat=n=3:v=1:a=1[outv][outa]"  -map "[outv]"
#
#
# ffmpeg -i videos/akI8YFjEmUw.mp4 -filter_complex "[0:v]trim=0:6.7,setpts=PTS-STARTPTS,setpts=PTS/3[v0]; [0:a]atrim=0:6.7,atempo=3[a0]; [0:v]trim=6.7:25.2,setpts=PTS-STARTPTS,setpts=PTS/1[v1]; [0:a]atrim=6.7:25.2,atempo=1[a1]; [0:v]trim=25.2:26,setpts=PTS-STARTPTS,setpts=PTS/3[v2]; [0:a]atrim=25.2:26,atempo=3[a2]; [0:v]trim=26:26.5,setpts=PTS-STARTPTS,setpts=PTS/3[v3]; [0:a]atrim=26:26.5,atempo=3[a3]; [0:v]trim=26.5:46.0,setpts=PTS-STARTPTS,setpts=PTS/1[v4]; [0:a]atrim=26.5:46.0,atempo=1[a4]; [0:v]trim=46.0:47.0,setpts=PTS-STARTPTS,setpts=PTS/3[v5]; [0:a]atrim=46.0:47.0,atempo=3[a5]; [0:v]trim=119.5:119.6,setpts=PTS-STARTPTS,setpts=PTS/3[v6]; [0:a]atrim=119.5:119.6,atempo=3[a6]; [0:v]trim=119.5:130.9,setpts=PTS-STARTPTS,setpts=PTS/1[v7]; [0:a]atrim=119.5:130.9,atempo=1[a7]; [0:v]trim=130.9:133,setpts=PTS-STARTPTS,setpts=PTS/3[v8]; [0:a]atrim=130.9:133,atempo=3[a8]; [v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5][v6][a6][v7][a7][v8][a8]concat=n=9:v=1:a=1[outv][outa]"  -map "[outv]" -map "[outa]" axxxx.mp4
