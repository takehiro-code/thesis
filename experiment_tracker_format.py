# this code will extract the values from the log

import argparse
import csv
import os
import pdb

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Running experiment')
    parser.add_argument("--input_path", help="input path for the output from the py-motmetrics", type=str)
    parser.add_argument("--output_path", help="output path to the data folder", type=str, default="data/")
    parser.add_argument("--class_cat", help="Select the class category", type=str)
    parser.add_argument("--seq_name", help="Select the sequence name", type=str)
    parser.add_argument("--class_id", help="Select object class_id", type=str)
    parser.add_argument("--qp", help="Select the QP value", type=int)
    parser.add_argument("--msr", help="Select the MSR value", type=int)
    parser.add_argument("--mAP", help="Pass the mAP value", type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    try:

        args = parse_args()
        input_path = args.input_path
        output_path = args.output_path
        try:
            # try converting to float
            mAP = float(args.mAP)
        except:
            # stay as String
            pass

        with open(input_path, 'r') as f:
            lines = f.readlines()

        line_split = lines[1].split()
        line_split = [element.replace('%','') for element in line_split]
        line_split = [element.replace('%','') for element in line_split]
        #seq_name = line_split[0]
        line_split.pop(0) # take out the first element which is ClassX_seqname_class_id
        param_list = [args.class_cat, args.seq_name, args.class_id, args.qp, args.msr, mAP]
        line_split_mod = param_list + line_split
        
        # if file doesn't exist, write a header first
        if not os.path.exists(output_path):
            with open(output_path, 'a', newline='') as f:
                header = lines[0].split()
                header.insert(0, "class_cat")
                header.insert(1, "seq_name")
                header.insert(2, "class_id")
                header.insert(3, "qp")
                header.insert(4, "msr")
                header.insert(5, "mAP")
                writer=csv.writer(f, delimiter=',')
                writer.writerow(header)
        
        with open(output_path, 'a', newline='') as f:
            writer=csv.writer(f, delimiter=',')
            writer.writerow(line_split_mod)

    except Exception as e:
        print(e)
        pdb.set_trace()
        pass