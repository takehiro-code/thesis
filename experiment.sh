
src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
out_dec_rgb_path=/local-scratch/tta46/thesis/video_comp/out_dec_rgb

# decoding
class_arr=('ClassB' 'ClassC' 'ClassD' 'ClassE')
class_arr=('ClassB')
qp_arr=(18 22 26 30 34 38)
msr_arr=(16 32 64)

for class_cat in ${class_arr[@]}
do
    if [ ${class_cat} == 'ClassB' ]
    then
        seq_name_arr=('BasketballDrive' 'Cactus' 'Kimono' 'ParkScene')
        # test stage
        resln='1920x1080'
        seq_name_arr=('BasketballDrive')
        qp_arr=(18)
        msr_arr=(16)
    elif [ ${class_cat} == 'ClassC' ]
    then
        seq_name_arr=('BasketballDrill' 'PartyScene' 'RaceHorsesC')
        resln='832x480'
    elif [ ${class_cat} == 'ClassD' ]
    then
        seq_name_arr=('BasketballPass' 'BlowingBubbles' 'RaceHorsesD')
        resln='416x240'
    elif [ ${class_cat} == 'ClassE' ]
    then
        seq_name_arr=('FourPeople' 'Johnny' 'KristenAndSara')
        resln='1280x720'
    else
        echo "Other classes not implemented"
        exit 0
    fi

    for seq_name in ${seq_name_arr[@]}
    do
        if [ ${seq_name} == 'BasketballDrive' ]
        then
            class_id_arr=(0 32 56 "all")
        elif [ ${seq_name} == 'Cactus' ]
        then
            class_id_arr=(58 "all")
        elif [ ${seq_name} == 'Kimono' ]
        then
            class_id_arr=(0 26 "all")
        elif [ ${seq_name} == 'ParkScene' ]
        then
            class_id_arr=(0 1 13 "all")
        elif [ ${seq_name} == 'BasketballDrill' ]
        then
            class_id_arr=(0 32 56 "all")
        elif [ ${seq_name} == 'PartyScene' ]
        then
            class_id_arr=(0 41 58 74 77 "all")
        elif [ ${seq_name} == 'RaceHorsesC' ]
        then
            class_id_arr=(0 17 "all")
        elif [ ${seq_name} == 'BasketballPass' ]
        then
            class_id_arr=(0 32 56 "all")
        elif  [ ${seq_name} == 'BlowingBubbles' ]
        then
            class_id_arr=(0 41 77 "all")
        elif [ ${seq_name} == 'RaceHorsesD' ]
        then
            class_id_arr=(0 17 "all")
        elif [ ${seq_name} == 'FourPeople' ]
        then
            class_id_arr=(0 41 56 58 "all")
        elif [ ${seq_name} == 'Johnny' ]
        then
            class_id_arr=(0 27 63 "all")
        elif [ ${seq_name} == 'KristenAndSara' ]
        then
            class_id_arr=(0 63 67 "all")
        else
            echo "Other sequence name not implemented"
            exit 0
        fi

        for qp in ${qp_arr[@]}
        do
            for msr in ${msr_arr[@]}
            do
                cd video_comp
                echo "decoding ${class_cat} ${seq_name} at qp=${qp}, msr=${msr}"
                out=${class_cat}_${seq_name}_qp${qp}_msr${msr}

                # first clean up the space
                rm out_dec/rec.yuv
                rm out_dec_rgb/*.png

                # decoding
                ./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec.yuv | tee out_log/log_${out}.txt
                
                # color conversion
                python3 yuv2png_converter.py\
                    --input out_dec/rec.yuv\
                    --resolution ${resln}\
                    --output_dir out_dec_rgb
                cd ..

                # running detector
                for class_id in ${class_id_arr[@]}
                do
                    if [ class_id == "all" ]
                    then
                        classes_filter=${class_id_arr[@]::${#class_id_arr[@]}-1} # all elements except last element
                    else
                        classes_filter=(class_id)
                    fi

                    cd yolov3
                    rm output/${class_cat}/${seq_name}/labels/*.txt
                    python3 detect.py\
                        --source ${out_dec_rgb_path}/\
                        --weights weights/yolov3.pt\
                        --conf-thres 0.25\
                        --iou-thres 0.55\
                        --img-size 640\
                        --save-conf\
                        --save-txt\
                        --classes ${classes_filter[@]}\
                        --project output/${class_cat}\
                        --name ${seq_name}\
                        --exist-ok
                    cd ..
                    
                    python3 yolo2mot.py\
                        --class_cat ${class_cat}\
                        --seq_name ${seq_name}\
                        --class_id ${class_id}
                    
                    cd sort
                    python3 sort.py\
                        --seq_path input/${class_cat}_${seq_name}_${class_id}\
                        --img_path ${out_dec_rgb_path}\
                        --max_age 1\
                        --min_hits 5\
                        --iou_threshold 0.4
                    cd ..
                    
                    mkdir -p py-motmetrics/res_dir_comp
                    
                    cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_comp/
                    
                    ## evaluate the performance
                    python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_comp/

                    ### 
                done
            done
        done
    done
done