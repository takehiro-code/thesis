# this code will extract the values from the log

import argparse
import csv
import os

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Running experiment')
    parser.add_argument("--input_path", help="Select the class category", type=str)
    parser.add_argument("--output_path", help="Select the class category", type=str)
    parser.add_argument("--max_age", help="Select the class category", type=int)
    parser.add_argument("--min_hits", help="Select the sequence name", type=int)
    parser.add_argument("--iou_thres", help="source path to the images", type=float)
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
    param_list = [args.max_age, args.min_hits, args.iou_thres]
    line_split_mod = param_list + line_split
    line_split_mod.insert(0,seq_name)
    
    # if file doesn't exist, write a header first
    if not os.path.exists(output_path):
        with open(output_path, 'a', newline='') as f:
            header = lines[0].split()
            header.insert(0, "seq_name")
            header.insert(1, "max_age")
            header.insert(2, "min_hits")
            header.insert(3, "iou_thres")
            writer=csv.writer(f, delimiter=',')
            writer.writerow(header)

    
    with open(output_path, 'a', newline='') as f:
        writer=csv.writer(f, delimiter=',')
        writer.writerow(line_split_mod)
