# Converting from yolo output format to mAP tool format

# load libraries
import glob
import numpy as np
from tqdm import tqdm
from skimage import io
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
    parser.add_argument("--source_path", help="source path to the images", type=str, default="/local-scratch/share_dataset/labled_hevc_sequences")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    #input
    args = parse_args()
    class_cat = args.class_cat # class category
    seq_name = args.seq_name # sequence name
    source_path = args.source_path

    # path construction
    img_path = f"{source_path}/{class_cat}/{seq_name}"
    input_path_gt = f"SFU-HW-Objects-v1_perfect/{class_cat}/{seq_name}/*.txt"
    output_gt_dir = f"temp/{class_cat}/{seq_name}"

    # read img dimension
    try:
        img = io.imread(glob.glob(f"{img_path}/*%03d.png"%(0))[0], plugin='matplotlib')
    except:
        img = io.imread(glob.glob(f"{img_path}/*.jpg")[0], plugin='matplotlib')
    img_h, img_w, _ = img.shape

    classmap = dict()
    obj_count = 0
    try:
        # ----------------------------------------------------------------
        # Convert GT files
        # ----------------------------------------------------------------
        print("Converting GT files to all categories case ...")
        alltxt = natural_sort(glob.glob(f"{input_path_gt}"))
        for txt in tqdm(alltxt):
            txt = txt.replace("\\","/")
            txt_name = txt.split("/")[-1]
            with open(f"{output_gt_dir}/{txt_name}", 'w') as output_file:
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


                # obj_id conversion for GT file, need some complex mapping algorithm
                data = np.array([frame_id, class_id, object_id, x, y, w, h, conf_arr, pos_x_3d, pos_y_3d, pos_z_3d]).T
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
                    (class_id, object_id, x, y, w, h)\
                        ), delimiter=' ', fmt="%d %d %s %s %s %s")

    except Exception as e:
        print(e)
        pdb.set_trace()
        pass
