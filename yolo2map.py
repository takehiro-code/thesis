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
    input_path = f"yolov3/output/{class_cat}/{seq_name}/labels/*.txt"
    output_dir = f"mAP/input/detection-results"
    input_path_gt = f"SFU-HW-Objects-v1_perfect/{class_cat}/{seq_name}/*.txt"
    output_gt_dir = f"mAP/input/ground-truth"

    # read img dimension
    try:
        img = io.imread(glob.glob(f"{img_path}/*%03d.png"%(0))[0], plugin='matplotlib')
    except:
        img = io.imread(glob.glob(f"{img_path}/*.jpg")[0], plugin='matplotlib')
    img_h, img_w, _ = img.shape

    try:
        # ----------------------------------------------------------------
        # Convert detection-results files
        # ----------------------------------------------------------------
        print("Converting yolo v3 output file to mAP format ...")
        alltxt = natural_sort(glob.glob(f"{input_path}"))
        for txt in tqdm(alltxt):
            txt = txt.replace("\\","/")
            txt_name = txt.split("/")[-1]
            with open(f"{output_dir}/{txt_name}", 'w') as output_file:
                class_id, x, y, w, h = np.genfromtxt(txt, unpack=True, encoding='utf_8_sig')

                # Either numpy array or single value if you read one row
                if isinstance(class_id, np.ndarray):
                    conf_arr = np.repeat(1, len(class_id))
                else:
                    conf_arr = 1

                # conversion of bbox
                x = normalize(x, 0, 1, 0, img_w)
                y = normalize(y, 0, 1, 0, img_h)
                w = normalize(w, 0, 1, 0, img_w)
                h = normalize(h, 0, 1, 0, img_h)

                # x1 y1 is top left, x2 y2 is bottom right
                x1 = x - w / 2
                y1 = y - h / 2
                x2 = x + w / 2
                y2 = y + h / 2

                # save into det file
                np.savetxt(output_file, np.column_stack(\
                    (class_id, conf_arr, x1, y1, x2, y2)\
                        ), delimiter=' ', fmt="%d %d %s %s %s %s")

        # ----------------------------------------------------------------
        # Convert GT files
        # ----------------------------------------------------------------
        print("Converting GT files to mAP format ...")
        alltxt = natural_sort(glob.glob(f"{input_path_gt}"))
        for txt in tqdm(alltxt):
            txt = txt.replace("\\","/")
            txt_name = txt.split("/")[-1]
            with open(f"{output_gt_dir}/{txt_name}", 'w') as output_file:
                class_id, object_id, x, y, w, h = np.genfromtxt(txt, unpack=True, encoding='utf_8_sig')

                # Either numpy array or single value if you read one row
                if isinstance(class_id, np.ndarray):
                    conf_arr = np.repeat(1, len(class_id))
                else:
                    conf_arr = 1

                # conversion of bbox
                x = normalize(x, 0, 1, 0, img_w)
                y = normalize(y, 0, 1, 0, img_h)
                w = normalize(w, 0, 1, 0, img_w)
                h = normalize(h, 0, 1, 0, img_h)

                # x1 y1 is top left, x2 y2 is bottom right
                x1 = x - w / 2
                y1 = y - h / 2
                x2 = x + w / 2
                y2 = y + h / 2

                # save into det file
                np.savetxt(output_file, np.column_stack(\
                    (class_id, x1, y1, x2, y2)\
                        ), delimiter=' ', fmt="%d %s %s %s %s")

    except Exception as e:
        print(e)
        pdb.set_trace()
        pass
