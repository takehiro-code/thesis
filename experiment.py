
# not going to work with subprocess and call

from subprocess import call

src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'

#decoding
class_arr = ['ClassB', 'ClassC', 'ClassD', 'ClassE']
qp_arr = [18, 22, 26, 30, 34, 38]
msr_arr = [16, 32, 64]

meta_data = {'ClassB': {'seq_name': {'BasketballDrive': [0, 32, 56, "all"],
                                     'Cactus': [58, "all"],
                                     'Kimono': [0, 26, "all"],
                                     'ParkScene': [0, 1, 13, "all"]},
                        'resolution': '1920x1080'},
             'ClassC': {'seq_name': {'BasketballDrill': [0, 32, 56, "all"],
                                     'PartyScene': [0, 41, 58, 74, 77, "all"],
                                     'RaceHorsesC': [0, 41, 58, 74, 77, "all"]},
                        'resolution': '832x480'},
             'ClassD': {'seq_name': {'BasketballPass': [0, 32, 56, "all"],
                                     'BlowingBubbles': [0, 41, 77, "all"],
                                     'RaceHorsesD': [0, 17, "all"]},
                        'resolution': '416x240'},
             'ClassE': {'seq_name': {'FourPeople': [0, 41, 56, 58, "all"],
                                     'Johnny': [0, 27, 63, "all"],
                                     'KristenAndSara': [0, 63, 67, "all"]},
                        'resolution': '1280x720'}
            }


for class_cat in meta_data:
    for seq_name in meta_data[class_cat]['seq_name']:
        for qp in qp_arr:
            for msr in msr_arr:
                #call(f"echo \"encoding {class_cat} {seq_name} at qp={qp}, msr={msr}\"")
                out = f"{class_cat}_{seq_name}_qp{qp}_msr{msr}"

                # # decoding operation
                # print(f"deconding {out}.bin ...")
                # call("cd video_comp")
                # call("rm out_dec/rec.yuv")
                # call("rm out_dec_rgb/*.png")
                # call(f"./TAppDecoderStatic -b out_bin/{out}.bin -o out_dec/rec.yuv | tee out_log/log_{out}.txt")
                
                # # yuv to rgb conversion
                # resolution = meta_data[class_cat]['resolution']
                # call(f"python3 yuv2png_converter.py\
                #      --input out_dec/rec.yuv\
                #      --resolution {resolution}\
                #      --output_dir out_dec_rgb")
                # call("cd ..")

                # call("cd yolov3")
                # call("rm output/${class_cat}/${seq_name}/labels/*.txt")













