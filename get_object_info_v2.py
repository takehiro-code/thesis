# this script will generate the .LIST files with one run
# this will also identify which frame has annotation error for duplicate object_id or id -1

import os
import numpy as np
import re
import pdb
import fnmatch # will be used with os.listdir to filter
import sys

dataset_path = "../SFU-HW-Tracks-v1"

dirs = {
    "ClassB": ["BasketballDrive", "Cactus", "Kimono", "ParkScene"],
    "ClassC": ["BasketballDrill", "PartyScene", "RaceHorsesC"],
    "ClassD": ["BasketballPass", "BlowingBubbles", "RaceHorsesD"],
    "ClassE": ["FourPeople", "Johnny", "KristenAndSara"]
}

coco_names = ['person', 'bicycle', 'car', 'motorbike', \
              'aeroplane', 'bus', 'train', 'truck', \
              'boat', 'traffic light', 'fire hydrant', 'stop sign', \
              'parking meter', 'bench' ,'bird', 'cat', \
              'dog', 'horse', 'sheep', 'cow', \
              'elephant', 'bear', 'zebra', 'giraffe', \
              'backpack', 'umbrella', 'handbag', 'tie', \
              'suitcase', 'frisbee', 'skis', 'snowboard', \
              'sports ball', 'kite', 'baseball bat', 'baseball glove', \
              'skateboard', 'surfboard', 'tennis racket', 'bottle', \
              'wine glass', 'cup', 'fork', 'knife',\
              'spoon', 'bowl', 'banana', 'apple', \
              'sandwich', 'orange', 'broccoli', 'carrot', \
              'hot dog', 'pizza', 'donut', 'cake', \
              'chair', 'sofa', 'pottedplant', 'bed', \
              'diningtable', 'toilet', 'tvmonitor', 'laptop', \
              'mouse', 'remote', 'keyboard', 'cell phone', \
              'microwave', 'oven', 'toaster', 'sink', \
              'refrigerator', 'book', 'clock', 'vase', \
              'scissors', 'teddy bear', 'hair drier', 'toothbrush']


if __name__ == "__main__":
    print("generating objects list files ...")

    # looping each directory in the dataset
    try:
        for class_cat in dirs:
            for seq_name in dirs[class_cat]:

                # get the list of frames name for only .txt files
                frame_list = fnmatch.filter(os.listdir(f"{dataset_path}/{class_cat}/{seq_name}"), '*.txt')

                # determining the name of the list file
                frame_list = np.array(frame_list)
                splits = re.split('_', frame_list[0])
                object_list = splits[0] + '_' + splits[1] + '_object.list'

                # set the file path to write
                seq_path =  f"{dataset_path}/{class_cat}/{seq_name}"
                wrt_file_path = f"{seq_path}/{object_list}"

                # delete the list file if it exists
                if os.path.isfile(wrt_file_path):
                    print(f"existing {object_list} exists, deleting it ...")
                    os.remove(wrt_file_path)

                # now creating a list file
                with open(wrt_file_path, 'w') as wrt_f:
                    overall_class_ids = []

                    # looping through each frame
                    for frame_idx, frame_name in enumerate(frame_list):
                        class_ids = []

                        # get the file path to the frame file
                        frame_path = f"{seq_path}/{frame_name}"

                        # reading the content of each frame file (actual ground truth)
                        with open(frame_path, "r") as ind_f:

                            # this dictionary is for checking annotation error
                            object_ids = {}
                            for object_info in ind_f:
                                class_id = int(re.split('\s+', object_info)[0])
                                object_id = int(re.split('\s+', object_info)[1])
                                
                                class_ids.append(class_id)
                                overall_class_ids.append(class_id)
                                
                                # adding object id to dictionary object_ids
                                if class_id not in object_ids:
                                    object_ids[class_id] = [object_id]
                                else:
                                    object_ids[class_id].append(object_id)


                        # check any annotation error
                        for class_id in object_ids:
                            # if object id duplicates exist or object id -1 exist
                            if ( len(object_ids[class_id]) != len(set(object_ids[class_id])) ) or (-1 in object_ids[class_id]):
                                print(f"Annotation Error in ground truth frame: {frame_path}")

                        class_ids = np.array(class_ids)

                        unique_classes, class_counts = np.unique(class_ids, return_counts=True)

                        wrt_f.write("In Frame {:03d} >> \n".format(frame_idx))
                        for class_id, counts in zip(unique_classes, class_counts):
                            wrt_f.write("\t#{} (Class ID:{}): {} \n".format(coco_names[class_id], class_id, counts))
                        wrt_f.write("\n")

                    unique_classes, class_counts = np.unique(overall_class_ids, return_counts=True)

                    wrt_f.write("\n\n")
                    wrt_f.write("Total frames : {}\n".format(len(frame_list)))
                    wrt_f.write("Total # classes : {}\n".format(len(unique_classes)))

                    for class_id, counts in zip(unique_classes, class_counts):
                        wrt_f.write("\t#{} (Class ID:{}): {} \n".format(coco_names[class_id], class_id, counts))
                    wrt_f.write("\n")

    except Exception as e:
        print("error occur!!!")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        pdb.set_trace()