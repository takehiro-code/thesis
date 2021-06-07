
# Converting from yolo output format to MOT challenge format

# load libraries
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from skimage import io
import cv2
import os
import argparse
import re
import pdb

def normalize(value, minValue, maxValue, a, b):
    return (value - minValue) / (maxValue - minValue) * (b - a) + a # normalize to [a, b] for drawing


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)



def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Running experiment')
    parser.add_argument("--class_cat", help="Select the class category", type=str)
    parser.add_argument("--seq_name", help="Select the sequence name", type=str)
    parser.add_argument("--class_id", help="Select the class ID", type=str) # str is default type
    parser.add_argument("--source_path", help="source path to the images", type=str, default="/local-scratch/share_dataset/labled_hevc_sequences")
    parser.add_argument("--test", help="test for public dataset",  action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    #input
    args = parse_args()
    class_cat = args.class_cat # class category
    seq_name = args.seq_name # sequence name
    class_cat_filter = args.class_id # object category # all doesn't work yet, in progress.
    source_path = args.source_path
    test_flag = args.test

    # set up directories
    if not os.path.exists("sort/input"):
        os.mkdir("sort/input")
    if not os.path.exists(f"sort/input/{class_cat}_{seq_name}_{class_cat_filter}"):
        os.mkdir(f"sort/input/{class_cat}_{seq_name}_{class_cat_filter}")
    if not os.path.exists(f"sort/input/{class_cat}_{seq_name}_{class_cat_filter}/det"):
        os.mkdir(f"sort/input/{class_cat}_{seq_name}_{class_cat_filter}/det")

    if not os.path.exists(f"py-motmetrics/gt_dir/{class_cat}_{seq_name}_{class_cat_filter}"):
        os.mkdir(f"py-motmetrics/gt_dir/{class_cat}_{seq_name}_{class_cat_filter}")
    if not os.path.exists(f"py-motmetrics/gt_dir/{class_cat}_{seq_name}_{class_cat_filter}/gt"):
        os.mkdir(f"py-motmetrics/gt_dir/{class_cat}_{seq_name}_{class_cat_filter}/gt")

    # path construction
    if source_path == "/local-scratch/share_dataset/labled_hevc_sequences":
        img_path = f"{source_path}/{class_cat}/{seq_name}"
    else:
        img_path = source_path
    # input_path = f"yolov3/output/{class_cat}/{seq_name}/labels/*.txt"
    output_path = f"sort/input/{class_cat}_{seq_name}_{class_cat_filter}/det/det.txt"
    input_path_gt = f"SFU-HW-Objects-v1_perfect/{class_cat}/{seq_name}/*.txt"
    output_path_gt = f"py-motmetrics/gt_dir/{class_cat}_{seq_name}_{class_cat_filter}/gt/gt.txt"

    # read img dimension
    try:
        img = io.imread(glob.glob(f"{img_path}/*%03d.png"%(0))[0], plugin='matplotlib')
    except:
        img = io.imread(glob.glob(f"{img_path}/*.jpg")[0], plugin='matplotlib')
    img_h, img_w, _ = img.shape

    try:
        if class_cat_filter == "all":
            
            # ----------------------------------------------------------------
            # Generate GT file with object id -1 in MOT format for all object categories
            # ----------------------------------------------------------------
            print("Converting yolo v3 output file in MOT format ...")
            alltxt = natural_sort(glob.glob(f"{input_path_gt}"))
            if os.path.exists(output_path):
                os.remove(output_path)
            with open(output_path, 'ab') as output_file:
                for txt in tqdm(alltxt):
                    if test_flag:
                        frame = int(txt.split("/")[-1].split(".")[0]) 
                    else:
                        frame = int(txt.split("_")[-1].split(".")[0]) + 1      
                    #print(f"for frame {frame} ...")
                    
                    data =  np.genfromtxt(txt, unpack=False, encoding='utf_8_sig')

                    # if data is empty at the frame XX
                    if data.size == 0:
                        # go to the next frame (next loop)
                        continue
                    class_id, object_id, x, y, w, h = data.T

                    # Either numpy array or single value if you read one row
                    if isinstance(class_id, np.ndarray):
                        frame_id = np.repeat(frame, len(class_id))
                        object_id = np.repeat(-1, len(class_id)) # no tracking, so assign -1
                        conf_arr = np.repeat(1, len(class_id)) # ground truth, so the detected confidence is 1
                        pos_x_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_y_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_z_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                    else:
                        frame_id = frame
                        object_id = -1 # no tracking, so assign -1
                        conf_arr = 1 # ground truth, so the detected confidence is 1
                        pos_x_3d = -1 # not 3d, so assign -1
                        pos_y_3d = -1 # not 3d, so assign -1
                        pos_z_3d = -1 # not 3d, so assign -1

                    # conversion of bbox
                    x = normalize(x, 0, 1, 0, img_w)
                    y = normalize(y, 0, 1, 0, img_h)
                    w = normalize(w, 0, 1, 0, img_w)
                    h = normalize(h, 0, 1, 0, img_h)

                    # x1 y1 is top left, x2 y2 is bottom right
                    x1 = x - w / 2
                    y1 = y - h / 2
                    # x2 = x + w / 2
                    # y2 = y + h / 2 
                      
                    # save into det file
                    np.savetxt(output_file, np.column_stack(\
                        (frame_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d)\
                            ), delimiter=',', fmt="%d,%d,%s,%s,%s,%s,%s,%d,%d,%d")
            

            # ----------------------------------------------------------------
            # Generate GT file in MOT format for all object categories
            # ----------------------------------------------------------------
            print("Converting GT file in MOT format ...")
            if test_flag:
                print("We don't convert public GT file!")
                exit()
            alltxt_gt = natural_sort(glob.glob(f"{input_path_gt}"))
            if os.path.exists(output_path_gt):
                os.remove(output_path_gt)
            classmap = dict()
            obj_count = 0
            with open(output_path_gt, 'ab') as output_file:
                for txt in tqdm(alltxt_gt):
                    frame = int(txt.split("_")[-1].split(".")[0]) + 1
                    class_id, object_id, x, y, w, h = np.genfromtxt(txt, unpack=True, encoding='utf_8_sig')
                    # no delmiter=' ' since the default is any whitespace

                    # Either numpy array or single value if you read one row
                    if isinstance(class_id, np.ndarray):
                        frame_id = np.repeat(frame, len(class_id))
                        conf_arr = np.repeat(1, len(class_id))
                        pos_x_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_y_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_z_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                    else:
                        frame_id = frame
                        conf_arr = 1
                        pos_x_3d = -1 # not 3d, so assign -1
                        pos_y_3d = -1 # not 3d, so assign -1
                        pos_z_3d = -1 # not 3d, so assign -1

                    # conversion of bbox
                    x = normalize(x, 0, 1, 0, img_w)
                    y = normalize(y, 0, 1, 0, img_h)
                    w = normalize(w, 0, 1, 0, img_w)
                    h = normalize(h, 0, 1, 0, img_h)

                    # x1 y1 is top left, x2 y2 is bottom right
                    x1 = x - w / 2
                    y1 = y - h / 2
                    # x2 = x + w / 2
                    # y2 = y + h / 2 

                    # obj_id conversion for GT file, need some complex mapping algorithm
                    data = np.array([frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d]).T
                    if data.ndim > 1:
                        # go through row by row
                        for i in range(len(data[:,1])):
                            # add new class id in classmap if it doesn't exist
                            if data[i,1] not in classmap:
                                classmap[data[i,1]] = dict()
                            old_obj_id = data[i,2]

                            # if old object id is in classmap[class_id] dictionary
                            # new object found!
                            if old_obj_id not in classmap[data[i,1]]:
                                obj_count += 1
                                new_obj_id = obj_count
                                data[i,2] = new_obj_id
                                classmap[data[i,1]][old_obj_id] = new_obj_id
                            # previously found object again
                            else:
                                new_obj_id = classmap[data[i,1]][old_obj_id]
                                data[i,2] = new_obj_id
                    
                    # in case of only 1 row of numpy array
                    else:
                        if data[1] not in classmap:
                            classmap[data[1]] = dict()
                        old_obj_id = data[2]
                        if old_obj_id not in classmap[data[1]]:
                            obj_count += 1
                            new_obj_id = obj_count
                            data[2] = new_obj_id
                            classmap[data[1]][old_obj_id] = new_obj_id
                        else:
                            new_obj_id = classmap[data[1]][old_obj_id]
                            data[2] = new_obj_id

                    frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d = data.T

                    # save into det file
                    np.savetxt(output_file, np.column_stack(\
                        (frame_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d)\
                            ), delimiter=',', fmt="%d,%d,%s,%s,%s,%s,%d,%d,%d,%d")
                    frame += 1

        else:
            # ----------------------------------------------------------------
            # Generate Generate GT file with object id -1 in MOT format
            # ----------------------------------------------------------------
            print("Converting yolo v3 output file in MOT format ...")
            class_cat_filter = int(class_cat_filter) # we have to use integer to filter numpy 2d array
            alltxt = natural_sort(glob.glob(f"{input_path_gt}"))
            if os.path.exists(output_path):
                os.remove(output_path)
            #frame = 1
            with open(output_path, 'ab') as output_file:
                for txt in tqdm(alltxt):
                    if test_flag:
                        frame = int(txt.split("/")[-1].split(".")[0]) 
                    else:
                        frame = int(txt.split("_")[-1].split(".")[0]) + 1      
                    #print(f"for frame {frame} ...")
                    data =  np.genfromtxt(txt, unpack=False, encoding='utf_8_sig')
                    
                    # if data is empty at the frame XX
                    if data.size == 0:
                        # go to the next frame (next loop)
                        continue
                    class_id, object_id, x, y, w, h = data.T

                    # Either numpy array or single value if you read one row
                    if isinstance(class_id, np.ndarray):
                        frame_id = np.repeat(frame, len(class_id))
                        object_id = np.repeat(-1, len(class_id)) # no tracking, so assign -1
                        conf_arr = np.repeat(1, len(class_id)) # ground truth, so the detected confidence is 1
                        pos_x_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_y_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_z_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                    else:
                        frame_id = frame
                        object_id = -1 # no tracking, so assign -1
                        conf_arr = 1 # ground truth, so the detected confidence is 1
                        pos_x_3d = -1 # not 3d, so assign -1
                        pos_y_3d = -1 # not 3d, so assign -1
                        pos_z_3d = -1 # not 3d, so assign -1

                    # conversion of bbox
                    x = normalize(x, 0, 1, 0, img_w)
                    y = normalize(y, 0, 1, 0, img_h)
                    w = normalize(w, 0, 1, 0, img_w)
                    h = normalize(h, 0, 1, 0, img_h)

                    # x1 y1 is top left, x2 y2 is bottom right
                    x1 = x - w / 2
                    y1 = y - h / 2
                    # x2 = x + w / 2
                    # y2 = y + h / 2 

                    # filtering by class_id
                    data = np.array([frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d]).T
                    if data.ndim > 1:
                        data = data[data[:,1]==class_cat_filter] # filtering by the class id
                    else:
                        if data[1] != class_cat_filter:
                            #frame += 1
                            continue
                    frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d = data.T
                        
                    # save into det file
                    np.savetxt(output_file, np.column_stack(\
                        (frame_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d)\
                            ), delimiter=',', fmt="%d,%d,%s,%s,%s,%s,%s,%d,%d,%d")
                    #frame += 1

            # ----------------------------------------------------------------
            # Generate GT file in MOT format
            # ----------------------------------------------------------------
            print("Converting GT file in MOT format ...")
            if test_flag:
                print("We don't convert public GT file!")
                exit()
            alltxt_gt = natural_sort(glob.glob(f"{input_path_gt}"))
            if os.path.exists(output_path_gt):
                os.remove(output_path_gt)
            #frame = 1
            with open(output_path_gt, 'ab') as output_file:
                for txt in tqdm(alltxt_gt):
                    frame = int(txt.split("_")[-1].split(".")[0]) + 1
                    class_id, object_id, x, y, w, h = np.genfromtxt(txt, unpack=True, encoding='utf_8_sig')
                    # no delmiter=' ' since the default is any whitespace

                    # Either numpy array or single value if you read one row
                    if isinstance(class_id, np.ndarray):
                        frame_id = np.repeat(frame, len(class_id))
                        conf_arr = np.repeat(1, len(class_id))
                        pos_x_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_y_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                        pos_z_3d = np.repeat(-1, len(class_id)) # not 3d, so assign -1
                    else:
                        frame_id = frame
                        conf_arr = 1
                        pos_x_3d = -1 # not 3d, so assign -1
                        pos_y_3d = -1 # not 3d, so assign -1
                        pos_z_3d = -1 # not 3d, so assign -1

                    # conversion of bbox
                    x = normalize(x, 0, 1, 0, img_w)
                    y = normalize(y, 0, 1, 0, img_h)
                    w = normalize(w, 0, 1, 0, img_w)
                    h = normalize(h, 0, 1, 0, img_h)

                    # x1 y1 is top left, x2 y2 is bottom right
                    x1 = x - w / 2
                    y1 = y - h / 2
                    # x2 = x + w / 2
                    # y2 = y + h / 2 

                    # filtering by class_id
                    data = np.array([frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d]).T
                    if data.ndim > 1:
                        data = data[data[:,1]==class_cat_filter] # filtering by the class id
                        data[:, 2] += 1 # increment object id by 1 to start from 1 not 0
                    else:
                        if data[1] != class_cat_filter:
                            #frame += 1
                            continue
                        else:
                            data[2] += 1 # increment object id by 1 to start from 1 not 0
                    frame_id, class_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d = data.T

                    # save into det file
                    np.savetxt(output_file, np.column_stack(\
                        (frame_id, object_id, x1, y1, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d)\
                            ), delimiter=',', fmt="%d,%d,%s,%s,%s,%s,%d,%d,%d,%d")
                    #frame += 1


    except Exception as e:
        print(e)
        print("Error!!")
        pdb.set_trace()
        pass
            

