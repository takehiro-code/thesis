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

# For plotting
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
plotly.offline.init_notebook_mode() # for exporting

# #uncertainties packages
# from uncertainties import ufloat
# from uncertainties.umath import *  #e.g. sqrt()
# from uncertainties import unumpy

# pd.options.display.float_format = '{:.2f}'.format

## probably not usable class_id: 26, 56
## ClassD RaceHorsesD experiment fails

## input
data_path = "../data"
input_path = f"{data_path}/experiment_result_v3.csv"
input_path_uncomp = f"{data_path}/experiment_uncompressed_result_v2.csv"
class_id = "all"
visual_metric = "MOTA"

seq_name_list = ['BasketballDrive','Cactus', 'Kimono', 'ParkScene',
        'BasketballDrill', 'RaceHorsesC',
        'BasketballPass', 'BlowingBubbles', 'RaceHorsesD',
        'FourPeople', 'Johnny', 'KristenAndSara']

for seq_name in seq_name_list:

    df = pd.read_csv(input_path, sep=',')
    df_uncomp = pd.read_csv(input_path_uncomp, sep=',')
    # df = pd.concat([df_uncomp, df_2.query('msr == 8 or msr == 16'), df.query('msr == 32 or msr == 64')])
    df = pd.concat([df_uncomp, df])
    df['F1'] = 2 * df['Prcn'] * df['Rcll'] / (df['Prcn'] + df['Rcll'])
    df['MOTP'] = ( 1 - df['MOTP'] ) * 100 
    header = ['class_cat', 'seq_name', 'class_id', 'qp', 'msr', 'idtp', 'idfp', 'idfn', 'IDF1', 'IDP', 'IDR',
            'Rcll', 'Prcn', 'F1', 'GT', 'MT', 'PT', 'ML', 'num_detections', 'FP', 'FN', 'IDs', 'FM', 'MOTA', 'MOTP']
    df = df[header] # re-arrange
    df.columns = ['class_cat', 'seq_name', 'class_id', 'QP', 'MSR', 'IDTP', 'IDFP', 'IDFN', 'IDF1', 'IDP', 'IDR',
            'Recall', 'Precision', 'F1', 'GT', 'MT', 'PT', 'ML', 'TP', 'FP', 'FN', 'IDs', 'FM', 'MOTA', 'MOTP']
    header = df.columns
    df = df[header]


    # ----------------------------------------------------------------------------------------------------
    # qp
    # ----------------------------------------------------------------------------------------------------
    df_seq = df[df['seq_name'] == seq_name]
    df_seq_cl = df_seq[df_seq['class_id'] == class_id]
    df_seq_cl_uncomp = df_seq_cl[df_seq_cl['MSR'] == 0].reset_index(drop=True)
    df_seq_cl_msr8 = df_seq_cl[df_seq_cl['MSR'] == 8]
    df_seq_cl_msr16 = df_seq_cl[df_seq_cl['MSR'] == 16]
    df_seq_cl_msr32 = df_seq_cl[df_seq_cl['MSR'] == 32]
    df_seq_cl_msr64 = df_seq_cl[df_seq_cl['MSR'] == 64]

    df_seq_cl_uncomp['QP'] = 'Uncompressed'
    df_seq_cl_uncomp['MSR'] = 'Uncompressed'


    fig = go.Figure()
    x_base = df_seq_cl_msr32['QP']
    y_const = [df_seq_cl_uncomp[visual_metric][0] for i in range(len(x_base))]
    fig.add_trace(go.Scatter(x=x_base, y=y_const,
                        mode='lines',
                        line=dict(dash='dash'),
                        name='Uncompressed'))
    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_msr8[visual_metric],
                        mode='lines+markers',
                        name='MSR=8'))
    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_msr16[visual_metric],
                        mode='lines+markers',
                        name='MSR=16'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_msr32[visual_metric],
                        mode='lines+markers',
                        name='MSR=32'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_msr64[visual_metric],
                        mode='lines+markers',
                        name='MSR=64'))
    x_name = "QP"
    y_name = visual_metric
    z_name = "MSR"
    fig.update_layout( font=dict(
                    color="black",
                    size=14),
                    xaxis_title=x_name,
                    yaxis_title=y_name)
    fig.show()
    fig.write_image(f"C:/OneDrive/SFU/ENSC498, 499/images/Appendix/{seq_name}_all_qp.pdf",width=1000, height=576)

    # ----------------------------------------------------------------------------------------------------
    # msr
    # ----------------------------------------------------------------------------------------------------

    df_seq = df[df['seq_name'] == seq_name]
    df_seq_cl = df_seq[df_seq['class_id'] == class_id]
    df_seq_cl_qp18 = df_seq_cl[df_seq_cl['QP'] == 18]
    df_seq_cl_qp22 = df_seq_cl[df_seq_cl['QP'] == 22]
    df_seq_cl_qp26 = df_seq_cl[df_seq_cl['QP'] == 26]
    df_seq_cl_qp30 = df_seq_cl[df_seq_cl['QP'] == 30]
    df_seq_cl_qp34 = df_seq_cl[df_seq_cl['QP'] == 34]
    df_seq_cl_qp38 = df_seq_cl[df_seq_cl['QP'] == 38]
    df_seq_cl_qp42 = df_seq_cl[df_seq_cl['QP'] == 42]
    df_seq_cl_qp46 = df_seq_cl[df_seq_cl['QP'] == 46]


    df_seq_cl_uncomp['QP'] = 'Uncompressed'
    df_seq_cl_uncomp['MSR'] = 'Uncompressed'




    fig = go.Figure()
    x_base = df_seq_cl_qp18['MSR']
    y_const = [df_seq_cl_uncomp[visual_metric][0] for i in range(len(x_base))]
    fig.add_trace(go.Scatter(x=x_base, y=y_const,
                        mode='lines',
                        line=dict(dash='dash'),
                        name='Uncompressed'))
    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_msr16[visual_metric],
                        mode='lines+markers',
                        name='QP=18'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp22[visual_metric],
                        mode='lines+markers',
                        name='QP=22'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp26[visual_metric],
                        mode='lines+markers',
                        name='QP=26'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp30[visual_metric],
                        mode='lines+markers',
                        name='QP=30'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp34[visual_metric],
                        mode='lines+markers',
                        name='QP=34'))

    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp38[visual_metric],
                        mode='lines+markers',
                        name='QP=38'))
    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp42[visual_metric],
                        mode='lines+markers',
                        name='QP=42'))
    fig.add_trace(go.Scatter(x=x_base, y=df_seq_cl_qp46[visual_metric],
                        mode='lines+markers',
                        name='QP=46'))
    x_name = "MSR"
    y_name = visual_metric
    z_name = "QP"
    fig.update_layout( font=dict(
                    color="black",
                    size=14),
                    xaxis_title=x_name,
                    yaxis_title=y_name)
    fig.show()
    fig.write_image(f"C:/OneDrive/SFU/ENSC498, 499/images/Appendix/{seq_name}_all_msr.pdf",width=1000, height=576)
