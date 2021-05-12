# load libraries
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
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

pd.options.display.float_format = '{:.2f}'.format

## probably not usable class_id: 26, 56

## input
data_path = "../data"
input_path = f"{data_path}/experiment_result_v3.csv"
input_path_uncomp = f"{data_path}/experiment_uncompressed_result_v2.csv"
class_id = "all"
visual_metric = "MOTA"
generate_figure = False

seq_name_list = ['BasketballDrive','Cactus', 'Kimono', 'ParkScene',
        'BasketballDrill', 'RaceHorsesC',
        'BasketballPass', 'BlowingBubbles', 'RaceHorsesD',
        'FourPeople', 'Johnny', 'KristenAndSara']

for seq_name in seq_name_list:
    if seq_name == 'BasketballDrive' or seq_name == 'Cactus' or seq_name == 'Kimono' or seq_name == 'ParkScene':
        class_cat = 'Class B'
    elif seq_name == 'BasketballDrill' or seq_name == 'RaceHorsesC':
        class_cat = 'Class C'
    elif seq_name == 'BasketballPass' or seq_name == 'BlowingBubbles' or seq_name == 'RaceHorsesD':
        class_cat = 'Class D'
    elif seq_name == 'FourPeople' or seq_name == 'Johnny' or seq_name == 'KristenAndSara':
        class_cat = 'Class E'
    else:
        print("error!")
        exit()

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

    if generate_figure:
        plt.style.use('seaborn-darkgrid')

        df_seq = pd.concat([df_seq_cl_msr8, df_seq_cl_msr16, df_seq_cl_msr32, df_seq_cl_msr64])

        fig, axs = plt.subplots(5, 4, figsize=(15,15))
        palette = plt.get_cmap('Set1')

        num = 0
        for row in range(5):
            for col in range(4):
                
                # plot uncompressed result
                x = df_seq.query('MSR == 8')['QP']
                metric = df_seq.iloc[:, 5+num].name
                y_const = [df_seq_cl_uncomp[metric] for i in range(len(x))]
                axs[row, col].set_title(metric)
                axs[row, col].plot(x, y_const, '--', label='Uncompressed')
                
                # plot metric
                y = df_seq.query('MSR == 8').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='MSR=8', color=palette(1))
                
                # plot metric
                y = df_seq.query('MSR == 16').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='MSR=16', color=palette(2))
                
                # plot metric
                y = df_seq.query('MSR == 32').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='MSR=32', color=palette(3))
                
                # plot metric
                y = df_seq.query('MSR == 64').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='MSR=64', color=palette(4))
                
            
                num += 1
                
                if row == 0 and col == 0:
                    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
                    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
                    fig.legend(lines, labels, loc=4, ncol=5, mode="", borderaxespad=.5,
                            frameon=True, bbox_to_anchor=(0., 1.02, 1., .102), fontsize='large')
                    # bbox_to_anchor=(0.125, 0.82, 1., .102)
                
        fig.tight_layout()
        plt.savefig(f"C:/OneDrive/SFU/ENSC498, 499/images/Appendix/{seq_name}_all_multiplots_qp.pdf", bbox_inches="tight")


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


    if generate_figure:
        plt.style.use('seaborn-darkgrid')

        df_seq = pd.concat([df_seq_cl_qp18, df_seq_cl_qp22, df_seq_cl_qp26,
                            df_seq_cl_qp30,df_seq_cl_qp34,df_seq_cl_qp38,
                            df_seq_cl_qp42, df_seq_cl_qp46])

        fig, axs = plt.subplots(5, 4, figsize=(15,15))
        # create a color palette
        palette = plt.get_cmap('Reds')

        num = 0
        for row in range(5):
            for col in range(4):
                
                
                # plot uncompressed result
                x = df_seq.query('QP == 18')['MSR']
                metric = df_seq.iloc[:, 5+num].name
                y_const = [df_seq_cl_uncomp[metric] for i in range(len(x))]
                axs[row, col].set_title(metric)
                axs[row, col].plot(x, y_const, '--', label='Uncompressed')
                
                # plot metric
                y = df_seq.query('QP == 18').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=18', color=palette(100))
                
                # plot metric
                y = df_seq.query('QP == 22').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=22', color=palette(90),)
                
                # plot metric
                y = df_seq.query('QP == 26').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=26', color=palette(80),)
                
                # plot metric
                y = df_seq.query('QP == 30').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=30', color=palette(70),)
                
                # plot metric
                y = df_seq.query('QP == 34').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=34', color=palette(60),)
                
                # plot metric
                y = df_seq.query('QP == 38').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=38', color=palette(50),)
                
                # plot metric
                y = df_seq.query('QP == 42').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=42', color=palette(40),)
                
                # plot metric
                y = df_seq.query('QP == 46').iloc[:, 5+num]
                axs[row, col].plot(x, y, '.-', label='QP=46', color=palette(30),)
                
                num += 1
                
                if row == 0 and col == 0:
                    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
                    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
                    fig.legend(lines, labels, loc=4, ncol=9, mode="", borderaxespad=.5,
                            frameon=True, bbox_to_anchor=(0.0, 1.02, 1., .102), fontsize='large')
                    # bbox_to_anchor=(0.125, 0.82, 1., .102) # panel on the right

        fig.tight_layout()
        plt.savefig(f"C:/OneDrive/SFU/ENSC498, 499/images/Appendix/{seq_name}_all_multiplots_msr.pdf", bbox_inches="tight")

    # ----------------------------------------------------------------------------------------------------
    # regression
    # ----------------------------------------------------------------------------------------------------

    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from sklearn.linear_model import LinearRegression

    df_all_avg = pd.concat([df_seq_cl_msr8, df_seq_cl_msr16, df_seq_cl_msr32, df_seq_cl_msr64])
    df_stats = pd.DataFrame([])
    # display(df_all_avg)
    header = ['QP', 'MSR', 'IDTP', 'IDFP', 'IDFN', 'IDF1', 'IDP', 'IDR',
            'Recall', 'Precision', 'F1', 'MT', 'PT', 'ML', 'TP', 'FP', 'FN', 'IDs', 'FM', 'MOTA', 'MOTP']
    df_all_avg = df_all_avg[header]

    for metric in df_all_avg:
        if metric != 'QP' and metric != 'MSR':
            result = smf.ols(formula=f"{metric} ~ QP + MSR + QP * MSR", data=df_all_avg).fit()
            series = result.params
            series['p-value(Intercept)'] =  result.pvalues[0]
            series['p-value(QP)'] =  result.pvalues[1]
            series['p-value(MSR)'] =  result.pvalues[2]
            series['p-value(QP:msr)'] =  result.pvalues[3]
            #series['rsquared'] = result.rsquared
            df_stats[metric] = series

    df_stats.index = ['coefficient(Intercept)', 'coefficient(QP)', 'coefficient(MSR)', 'coefficient(QP*MSR)',
                    'p-value(Intercept)', 'p-value(QP)', 'p-value(MSR)', 'p-value(QP*MSR)']


    # ----------------------------------------------------------------------------------------------------
    # latex code generator
    # ----------------------------------------------------------------------------------------------------


    out_path = f"C:/OneDrive/SFU/ENSC498, 499/images/Appendix/tex/{seq_name}_all.tex"
    with open(out_path, 'w') as f:

        # latex code
        tex = f"""
\\section{{{class_cat} {seq_name}}}
\\label{{sec:appendix/{seq_name}_all}}


% visualization figure
\\begin{{figure}}[!htbp]
\\centering
\\includegraphics[width=1.0\linewidth]{{img/appendix/{seq_name}_all_multiplots_qp.pdf}}
\\caption[Visualization of performance results in {class_cat} {seq_name} at different QP]
{{Visualization of performance results in {class_cat} {seq_name} at different QP.}}
\\label{{fig:{seq_name}_all_qp}}
\\end{{figure}}

\\begin{{figure}}[!htbp]
\\centering
\\includegraphics[width=1.0\linewidth]{{img/appendix/{seq_name}_all_multiplots_msr.pdf}}
\\caption[Visualization of performance results in {class_cat} {seq_name} at different MSR]
{{Visualization of performance results in {class_cat} {seq_name} at different MSR.}}
\\label{{fig:{seq_name}_all_msr}}
\\end{{figure}}



% table
\\begin{{table}}
\\centering
\\caption[Performance results in {class_cat} {seq_name}]
{{Performance results in {class_cat} {seq_name}.}}


% table for uncompressed
\\begin{{subtable}}[t]{{\linewidth}}
\\centering
\\vspace{{0pt}}
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_seq_cl_uncomp.iloc[:,3:].to_latex(index=False, multirow=True)}
}}
\\caption{{Uncompressed Sequence}}
\\end{{subtable}}


% table for msr=8
\\begin{{subtable}}[t]{{\linewidth}}
\\centering
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_seq_cl_msr8.iloc[:,3:].to_latex(index=False, multirow=True)}
}}
\\caption{{MSR = 8}}
\\end{{subtable}}



% table for msr=16
\\begin{{subtable}}[t]{{\linewidth}}
\\centering
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_seq_cl_msr16.iloc[:,3:].to_latex(index=False, multirow=True)}
}}
\\caption{{MSR = 16}}
\\end{{subtable}}


% table for msr=32
\\begin{{subtable}}[t]{{\linewidth}}
\\centering
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_seq_cl_msr32.iloc[:,3:].to_latex(index=False, multirow=True)}
}}
\\caption{{MSR = 32}}
\\end{{subtable}}


% table for msr=64
\\begin{{subtable}}[t]{{\linewidth}}
\\centering
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_seq_cl_msr64.iloc[:,3:].to_latex(index=False, multirow=True)}
}}
\\caption{{MSR = 64}}
\\end{{subtable}}


\\label{{tab:{seq_name}_all}}
\\end{{table}}




\\begin{{table}}[!htbp]
\\centering
\\caption[Multiple linear regression analysis result for {class_cat} {seq_name}]
{{Multiple linear regression analysis result for {class_cat} {seq_name}}}
\\resizebox{{1.0\linewidth}}{{!}}{{
{df_stats.to_latex(index=True, multirow=True)}
}}
\\label{{tab:{seq_name}_all_reg}}
\\end{{table}}

"""
        print(tex ,file=f)