
src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'
rgb_source_path='/local-scratch/share_dataset/labled_hevc_sequences'
yuv_source_path='/local-scratch/chyomin/HEVC_Common_Test_Sequence'
test_source_path='/local-scratch/tta46/thesis/seq_test'
out_dec_rgb_path='/local-scratch/tta46/thesis/video_comp/out_dec_rgb'

output_path='data/experiment_uncomp-06-05-2021.csv'

#prepare and clean up
mkdir -p py-motmetrics/res_dir_comp
rm ${output_path}
sleep 2

uuid=$(uuidgen) # unique identifier

class_arr=('ClassB' 'ClassC' 'ClassD' 'ClassE')
# class_arr=('ClassB' 'ClassD' 'ClassE') # part of the experiment
class_arr=('ClassD')

qp=0 # actually not qp=0, but rather uncompressed
msr=0 # actually not msr=0, but rather uncompressed

for class_cat in ${class_arr[@]}
do
    if [ ${class_cat} == 'ClassB' ]
    then
        seq_name_arr=('BasketballDrive' 'Cactus' 'Kimono' 'ParkScene')
        # seq_name_arr=('Cactus') # for individual analysis
        resln='1920x1080'
    elif [ ${class_cat} == 'ClassC' ]
    then
        seq_name_arr=('BasketballDrill' 'RaceHorsesC') # excluded training sequence
        resln='832x480'
    elif [ ${class_cat} == 'ClassD' ]
    then
        seq_name_arr=('BasketballPass' 'BlowingBubbles' 'RaceHorsesD')
        # seq_name_arr=('BasketballPass' 'BlowingBubbles') # for individual analysis
        resln='416x240'
    elif [ ${class_cat} == 'ClassE' ]
    then
        seq_name_arr=('FourPeople' 'Johnny' 'KristenAndSara')
        # seq_name_arr=('Johnny') # for individual analysis
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
            yuv_name="BasketballDrive_1920x1080_50.yuv"
        elif [ ${seq_name} == 'Cactus' ]
        then
            class_id_arr=(58 "all")
            # class_id_arr=(58) # for individual analysis
            yuv_name="Cactus_1920x1080_50.yuv"
        elif [ ${seq_name} == 'Kimono' ]
        then
            class_id_arr=(0 26 "all")
            yuv_name="Kimono1_1920x1080_24.yuv"
        elif [ ${seq_name} == 'ParkScene' ]
        then
            class_id_arr=(0 1 13 "all")
            yuv_name="ParkScene_1920x1080_24.yuv"
        elif [ ${seq_name} == 'BasketballDrill' ]
        then
            class_id_arr=(0 32 56 "all")
            yuv_name="BasketballDrill_832x480_50.yuv"
        elif [ ${seq_name} == 'PartyScene' ]
        then
            class_id_arr=(0 41 58 74 77 "all")
            yuv_name="PartyScene_832x480_50.yuv"
        elif [ ${seq_name} == 'RaceHorsesC' ]
        then
            class_id_arr=(0 17 "all")
            yuv_name="RaceHorses_832x480_30.yuv"
        elif [ ${seq_name} == 'BasketballPass' ]
        then
            class_id_arr=(0 32 56 "all")
            # class_id_arr=(0) # for individual analysis
            yuv_name="BasketballPass_416x240_50.yuv"
        elif  [ ${seq_name} == 'BlowingBubbles' ]
        then
            class_id_arr=(0 41 77 "all")
            # class_id_arr=(0) # for individual analysis
            yuv_name="BlowingBubbles_416x240_50.yuv"
        elif [ ${seq_name} == 'RaceHorsesD' ]
        then
            class_id_arr=(0 17 "all")
            yuv_name="RaceHorses_416x240_30.yuv"
        elif [ ${seq_name} == 'FourPeople' ]
        then
            class_id_arr=(0 41 56 58 "all")
            yuv_name="FourPeople_1280x720_60.yuv"
        elif [ ${seq_name} == 'Johnny' ]
        then
            class_id_arr=(0 27 63 "all")
            # class_id_arr=(0) # for individual analysis
            yuv_name="Johnny_1280x720_60.yuv"
        elif [ ${seq_name} == 'KristenAndSara' ]
        then
            class_id_arr=(0 63 67 "all")
            yuv_name="KristenAndSara_1280x720_60.yuv"
        else
            echo "Other sequence name not implemented"
            exit 0
        fi

        #color conversion
        cd video_comp
        rm out_dec_rgb/*.png
        sleep 2
        python3 yuv2png_converter.py\
            --input ${yuv_source_path}/${class_cat}/${yuv_name}\
            --resolution ${resln}\
            --output_dir out_dec_rgb
        sleep 2
        cd ..

        # running detector
        for class_id in ${class_id_arr[@]}
        do
            if [ ${class_id} == "all" ]
            then
                classes_filter=${class_id_arr[@]::${#class_id_arr[@]}-1} # all elements except last element
            else
                classes_filter=(${class_id})
            fi

            cd yolov3
            rm output/${class_cat}/${seq_name}/labels/*.txt
            sleep 2
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
            sleep 2
            cd ..

            # copying the det results to the folder for backup
            mkdir -p data/det_results/${class_cat}_${seq_name}_${class_id}_uncompressed
            rm data/det_results/${class_cat}_${seq_name}_${class_id}_uncompressed/*.txt
            sleep 2
            cp yolov3/output/${class_cat}/${seq_name}/labels/*.txt data/det_results/${class_cat}_${seq_name}_${class_id}_uncompressed
            sleep 2

            # convert to YOLO format to PASCAL VOC format for mAP measurement
            conf=0.25
            iou=0.55
            img_s=640
            rm mAP/input/detection-results/*.txt
            sleep 2
            rm mAP/input/ground-truth/*.txt
            sleep 2
            python3 -W ignore yolo2map.py\
            --class_cat $class_cat\
            --seq_name $seq_name\
            --class_id ${class_id}\
            --source_path $out_dec_rgb_path
            sleep 2

            # evaluating mAP@50
            cd mAP
            mAP=`python3 main.py -na -np -q\
            --class_cat ${class_cat}\
            --seq_name ${seq_name}\
            --class_id ${class_id}\
            --conf_thres ${conf}\
            --iou_thres ${iou}\
            --img_size ${img_s}`
            cd ..

            # converting YOLO to MOT format
            python3 -W ignore yolo2mot.py\
                --class_cat ${class_cat}\
                --seq_name ${seq_name}\
                --class_id ${class_id}\
                --source_path ${out_dec_rgb_path}
            sleep 2
            
            ## uncomment this to generate the video 
            # vid_dir_name=${class_cat}_${seq_name}_${class_id}_uncomp
            # mkdir -p data/vid/${vid_dir_name}
            cd sort
            python3 sort.py\
                --seq_path input/${class_cat}_${seq_name}_${class_id}\
                --img_path ${out_dec_rgb_path}/\
                --max_age 1\
                --min_hits 5\
                --iou_threshold 0.4
            sleep 2

            ## use the following to generate the video
            # python3 sort.py\
            #     --seq_path input/${class_cat}_${seq_name}_${class_id}\
            #     --img_path ${out_dec_rgb_path}/\
            #     --max_age 1\
            #     --min_hits 5\
            #     --iou_threshold 0.4\
            #     --display\
            #     --vid_dir_path ../data/vid/${vid_dir_name}
            # sleep 2
            cd ..

            # clean up the result folder from py-motmetrics
            rm py-motmetrics/res_dir_comp/*.txt
            sleep 2
            
            cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_comp/
            sleep 2
            cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir/ # keep copy in res_dir
            sleep 2
            
            ## evaluate the performance
            python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_comp/ > data/one_iter_${uuid}.txt
            sleep 2

            # extracting values
            python3 experiment_tracker_format.py\
                --input_path data/one_iter_${uuid}.txt\
                --output_path ${output_path}\
                --class_cat ${class_cat}\
                --seq_name ${seq_name}\
                --class_id ${class_id}\
                --qp ${qp}\
                --msr ${msr}\
                --mAP ${mAP}
            sleep 2


            ## use this to test the only 1 iteration in the loop
            # rm data/one_iter_${uuid}.txt
            # exit
        done
    done
done

rm data/one_iter_${uuid}.txt
sleep 2