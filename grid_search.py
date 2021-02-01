import glob
import numpy as np
from tqdm import tqdm
from skimage import io
import os
import argparse
import re
import pdb

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Running experiment')
    parser.add_argument("--input_path", help="Select the input path", type=str)
    args = parser.parse_args()
    return args


def pprint(A):
    if A.ndim==1:
        print(A)
    else:
        w = max([len(str(s)) for s in A]) 
        print(u'\u250c'+u'\u2500'*w+u'\u2510') 
        for AA in A:
            print(' ', end='')
            print('[', end='')
            for i,AAA in enumerate(AA[:-1]):
                w1=max([len(str(s)) for s in A[:,i]])
                print(str(AAA)+' '*(w1-len(str(AAA))+1),end='')
            w1=max([len(str(s)) for s in A[:,-1]])
            print(str(AA[-1])+' '*(w1-len(str(AA[-1]))),end='')
            print(']')
        print(u'\u2514'+u'\u2500'*w+u'\u2518')


if __name__ == '__main__':
    args = parse_args()
    input_path = args.input_path
    conf_thres, iou_thres, img_size, mAP = np.genfromtxt(input_path, delimiter=',', unpack=True, encoding='utf_8_sig')

    highest_mAP = np.max(mAP)

    # filtering by class_id
    data = np.array([conf_thres, iou_thres, img_size, mAP]).T
    data = data[data[:,3]==highest_mAP] # filtering by highest mAP
    conf_thres, iou_thres, img_size, mAP = data.T
    print(f"conf_thres, iou_thres, img_size, mAP")
    pprint(data)
    print(f"conf_thres: {conf_thres}\niou_thres: {iou_thres}\nimg_size: {img_size}\nhighest_mAP: {highest_mAP}")


