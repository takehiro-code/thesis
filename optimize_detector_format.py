# this code will extract the values from the log

import argparse
import csv
import os

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Running experiment')
    parser.add_argument("--input_path", help="Select the class category", type=str)
    parser.add_argument("--output_path", help="Select the class category", type=str)
    parser.add_argument("--conf_thres", help="Select the class category", type=float)
    parser.add_argument("--iou_thres", help="Select the sequence name", type=float)
    parser.add_argument("--img_size", help="source path to the images", type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    input_path = args.input_path
    output_path = args.output_path

    with open(input_path, 'r') as f:
        lines = f.readlines()

    line_split = lines[1].split()
    line_split = [element.replace('%','') for element in line_split]
    line_split = [element.replace('%','') for element in line_split]
    seq_name = line_split[0]
    line_split.pop(0)
    param_list = [args.conf_thres, args.iou_thres, args.img_size]
    line_split_mod = param_list + line_split
    line_split_mod.insert(0,seq_name)
    
    # if file doesn't exist, write a header first
    if not os.path.exists(output_path):
        with open(output_path, 'a', newline='') as f:
            header = lines[0].split()
            header.insert(0, "seq_name")
            header.insert(1, "conf_thres")
            header.insert(2, "iou_thres")
            header.insert(3, "img_size")
            writer=csv.writer(f, delimiter=',')
            writer.writerow(header)

    
    with open(output_path, 'a', newline='') as f:
        writer=csv.writer(f, delimiter=',')
        writer.writerow(line_split_mod)
