import cv2
import time
import os
import numpy as np

all_frames = []


def video_to_frames(input_loc):
    # Log the time
    all_frames=[]
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print("Number of frames: ", video_length)
    count = 0
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    print(fps)
    print("Converting video..\n")

    total_seconds=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))

    # Start converting the video
    while cap.isOpened():
        ret, frame = cap.read()
        if (count % fps == 0):
            all_frames.append(frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length - 1)):
            time_end = time.time()
            cap.release()
            # Print stats
            print("Done extracting frames.\n%d frames extracted" % count)
            print("It took %d seconds forconversion." % (time_end - time_start))

            break
    return all_frames,total_seconds


def get_orb_ratios(filepath):
    all_frames,total_seconds=video_to_frames(filepath)
    orb = cv2.ORB_create(nfeatures=10000)

    all_descriptors=[]
    for i in range(len(all_frames)):
        img=all_frames[i]
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        kp, des = orb.detectAndCompute(img,None)
        all_descriptors.append(des)

    orb_ratios=[]
    for i in range(len(all_frames)-1):
        if(all_descriptors[i] is None or all_descriptors[i+1] is None):
            orb_ratios.append(0)
        else:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(all_descriptors[i],all_descriptors[i+1])
            len(all_descriptors[i])
            len(all_descriptors[i+1])
            len(matches)
            orb_ratios.append(len(matches)/(len(all_descriptors[i])+len(all_descriptors[i+1])))
        print(i,end=" ")
    print()

    return orb_ratios,total_seconds



def boundary_detection(dist_list):
    #     print(dist_list)
    threshold = 0.5
    boundaries = []
    for i in range(1, len(dist_list) - 1):
        if dist_list[i] < dist_list[i - 1] and dist_list[i] < dist_list[i + 1]:

            prev_peak = i - 1
            next_peak = i + 1
            while (prev_peak != 0 and dist_list[prev_peak] < dist_list[prev_peak - 1]):
                prev_peak -= 1
            while (next_peak != len(dist_list) and dist_list[next_peak] < dist_list[next_peak - 1]):
                next_peak += 1
            #             print(dist_list[i]*2,dist_list[prev_peak],dist_list[next_peak])
            if dist_list[i] < dist_list[prev_peak] * threshold or dist_list[i] < dist_list[next_peak] * threshold:
                boundaries.append(i)
    #                 print(i)

    return boundaries

def get_boundaries(orb_ratios,total_seconds):
    orb_boundaries=boundary_detection(orb_ratios)
    orb_boundaries.insert(0, 0)
    orb_boundaries.insert(len(orb_boundaries), total_seconds)
    return orb_boundaries



