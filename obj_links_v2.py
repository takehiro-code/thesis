from __future__ import print_function

import argparse
import re
import numpy as np

import os
import matplotlib.pyplot as plt

from skimage import io
from skimage.transform import rescale, resize
from skimage.metrics import structural_similarity
from pytorch_msssim import ssim, ms_ssim, SSIM, MS_SSIM
import torch
#import tensorflow as tf


from tqdm import tqdm
import pdb

def visualize_patches(patch1, patch2, frm_no, cur_obj, prv_obj, best_ncc):
    fig, axes = plt.subplots(ncols=2)
    ax = axes.ravel()

    ax[0].imshow(patch1)
    ax[0].set_title(f"Cur. Patch in Frm {frm_no}\n class_id: {cur_obj['class_id']}\n proposed obj_id: {prv_obj['obj_id']}\n centre_x: {cur_obj['centre_x']}\n centre_y: {cur_obj['centre_y']}")
    ax[1].imshow(patch2)
    ax[1].set_title(f"Prv. Patch in Frm {frm_no-1}\n class_id: {prv_obj['class_id']}\n obj_id: {prv_obj['obj_id']}\n centre_x: {prv_obj['centre_x']}\n centre_y: {prv_obj['centre_y']}")
    plt.tight_layout()
    plt.show()

def get_roi(img, obj_info):
    # image shape [height, width, channel]
    # coordinates are all normalized with respect to the image resolution
    img_h, img_w, _ = img.shape

    bbox_w = obj_info['bbox_width']
    bbox_h = obj_info['bbox_height']

    top_left_x = obj_info['centre_x'] - bbox_w/2
    top_left_y = obj_info['centre_y'] - bbox_h/2

    top_left_y_pixelPos = int(top_left_y * img_h)
    bottom_left_y_pixelPos = int((top_left_y + bbox_h) * img_h)
    top_left_x_pixelPos = int(top_left_x * img_w)
    top_right_x_pixelPos = int((top_left_x + bbox_w) * img_w)

    # if part of patch go beyond the image shape, set to pixel position at the edges
    if top_left_y_pixelPos < 0:
        top_left_y_pixelPos = 0
    if bottom_left_y_pixelPos > img_h:
        bottom_left_y_pixelPos = img_h
    if top_left_x_pixelPos < 0:
        top_left_x_pixelPos = 0
    if top_right_x_pixelPos > img_w:
        top_right_x_pixelPos = img_w

    return img[top_left_y_pixelPos:bottom_left_y_pixelPos, top_left_x_pixelPos:top_right_x_pixelPos,:]


def get_ncc(patch1, patch2):
    p1_mean = patch1.mean()
    p2_mean = patch2.mean()

    p1 = (patch1 - p1_mean)
    p2 = (patch2 - p2_mean)

    #print(p1.shape, p2.shape)

    numerator = np.sum(p1 * p2)
    #print(numerator.shape)

    denominator = np.sqrt(np.sum(p1**2)*np.sum(p2**2))
    #print(denominator.shape)

    return numerator / denominator


def generate_output_files(file_name, object_lists):
    print("Write Output to {}.txt".format(file_name))

    #for obj in object_lists:
    #    print("{} {} {} {} {} {}\n".format(int(obj['class_id']), int(obj['obj_id']), float(obj['centre_x']), float(obj['centre_y']), float(obj['bbox_width']), float(obj['bbox_height'])))
        #print(obj)
    with open(file_name+'.txt', 'w') as f:
        for obj in object_lists:
            f.write("{} {} {} {} {} {}\n".format(int(obj['class_id']), int(obj['obj_id']), float(obj['centre_x']), float(obj['centre_y']), float(obj['bbox_width']), float(obj['bbox_height'])))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("text_list", nargs="?", help = "list of individual groundtruth files for a sequence")

    args = parser.parse_args()

    file_list = []
    with open(args.text_list,"r") as f:
        for line in f:
            file_name_wo_ext = line.strip().split('.')[0]
            if os.path.exists(file_name_wo_ext +'.png'):
                file_list.append(file_name_wo_ext)
            else:
                print("Relevant file doesn't exist\n")


    print("Total frames: {}".format(len(file_list)))

    for i, file_name in tqdm(enumerate(file_list)):
        print("Test File : {}".format(file_name))

        object_lists = []
        with open(file_name+".txt","r") as f:
            for line in f:
                seps = line.strip().split(' ')
                if len(seps) == 5:
                    new_dict = dict([('class_id', int(seps[0])), ('obj_id', -1), ('centre_x', float(seps[1])), ('centre_y', float(seps[2])), ('bbox_width', float(seps[3])), ('bbox_height', float(seps[4]))])
                elif len(seps) == 6:
                    new_dict = dict([('class_id', int(seps[0])), ('obj_id', -1), ('centre_x', float(seps[2])), ('centre_y', float(seps[3])), ('bbox_width', float(seps[4])), ('bbox_height', float(seps[5]))])
                else:
                    print("Ground truth file has illegal number of elements. It should be either 5 or 6.")
                    exit()
                object_lists.append(new_dict)

                #print(new_dict)
        print("\tTotal objects: {}".format(len(object_lists)))

        if i == 0:
            print("\tInitialize object ids for the first frame")
            prev_class_id = -1
            obj_id_cnt = -1
            for obj in sorted(object_lists, key = lambda k: k['class_id']):
                if prev_class_id != obj['class_id']:
                    obj_id_cnt = 0
                else :
                    obj_id_cnt+=1

                obj['obj_id'] = obj_id_cnt
                prev_class_id = obj['class_id']


        else:
            cur_image = io.imread(file_name+'.png', plugin='matplotlib')
            prv_image = io.imread(prev_file_name+'.png', plugin='matplotlib')

            for cur_obj in sorted(object_lists, key = lambda k: k['class_id']):

                cur_obj_patch = get_roi(cur_image, cur_obj)

                best_ncc = -1.0
                best_match_obj = []
                matched_patch = []
                for prv_obj in sorted(prev_object_lists, key = lambda k:k['class_id']):
                    if cur_obj['class_id'] == prv_obj['class_id']:
                        prv_obj_patch = get_roi(prv_image, prv_obj)

                        resized_prv_obj_patch = resize(prv_obj_patch, cur_obj_patch.shape, anti_aliasing=True)

                        # Compare
                        ncc_cost = get_ncc(cur_obj_patch, resized_prv_obj_patch)
                        #ncc_cost = structural_similarity(cur_obj_patch, resized_prv_obj_patch, multichannel=True)
                        
                        """                        
                        img1 = torch.tensor(cur_obj_patch)
                        img2 = torch.tensor(resized_prv_obj_patch                       
                        img1 = np.transpose(img1, (2, 0, 1)
                        img2 = np.transpose(img2, (2, 0, 1)                      
                        img1 = img1.unsqueeze(0
                        img2 = img2.unsqueeze(0)                       
                        print(img1.shape, img2.shape)
                        ncc_cost = ms_ssim( img1,  img2, data_range=1, size_average=False ) #(N,)
                        """

                        if ncc_cost > best_ncc:
                            best_ncc = ncc_cost
                            best_match_obj = prv_obj
                            matched_patch  = resized_prv_obj_patch
                        ##print(ncc_cost)
                        #visualize_patches(cur_obj_patch, resized_prv_obj_patch, i)

                #print("Best ncc cost:{:.04f}".format(best_ncc))
                #if i > 17 and i < 20:
                #    print(best_ncc)
                #    print(best_match_obj)
                #    visualize_patches(cur_obj_patch, matched_patch, i)

                # Assign obj id to the tartget obj
                if best_ncc >= 0.60:
                    #if i == 439:
                    #visualize_patches(cur_obj_patch, matched_patch, i, cur_obj, best_match_obj, best_ncc)
                    
                    if best_match_obj['obj_id'] == -1:
                      visualize_patches(cur_obj_patch, matched_patch, i, cur_obj, best_match_obj, best_ncc)
                      try:
                        userInput = input(f"Enter the correct object id (proposed id is {best_match_obj['obj_id']}): ")
                        cur_obj['obj_id'] = userInput
                      except Exception as e:
                        print(e)
                        print("Exiting program ...")
                        exit()
                    else:
                      cur_obj['obj_id'] = best_match_obj['obj_id']
                    print(f"frm {i} - best_ncc {best_ncc}")
                elif best_ncc != -1:
                    visualize_patches(cur_obj_patch, matched_patch, i, cur_obj, best_match_obj, best_ncc)
                    #cur_obj['obj_id'] = best_match_obj['obj_id']
                    print(f"frm {i} - best_ncc {best_ncc}. Found matched object with lower confidence Frm : {i} with {best_ncc} - OBJ: {cur_obj['class_id']} { cur_obj['centre_x']} {cur_obj['centre_y']} {cur_obj['bbox_width']} {cur_obj['bbox_height']}")
                    
                    try:
                      userInput = input(f"Enter the correct object id (proposed id is {best_match_obj['obj_id']}): ")
                      cur_obj['obj_id'] = userInput
                      print()
                    except Exception as e:
                      print(e)
                      print("Exiting program ...")
                      exit()
                else:
                    print("Cannot find any matched object Frm : {} - OBJ: {} {} {} {} {}".format(i, cur_obj['class_id'], cur_obj['centre_x'], cur_obj['centre_y'], cur_obj['bbox_width'], cur_obj['bbox_height']))
                    if cur_obj['obj_id'] == -1:
                      try:
                        userInput = input(f"Enter the correct object id (proposed id is {cur_obj['obj_id']}): ")
                        cur_obj['obj_id'] = userInput
                        print()
                      except Exception as e:
                        print(e)
                        print("Exiting program ...")
                        exit()

        # print
        #for obj in object_lists:
        #    print(obj)

        try:
          generate_output_files(file_name, object_lists)
        except Exception as e:
          print(e)
          print("Exiting program ...")
          exit()

        prev_object_lists = object_lists
        prev_file_name    = file_name

