
src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'
rgb_source_path='/local-scratch/share_dataset/labled_hevc_sequences'
yuv_source_path='/local-scratch/chyomin/HEVC_Common_Test_Sequence'
test_source_path='/local-scratch/tta46/thesis/seq_test'
out_dec_rgb_path='/local-scratch/tta46/thesis/video_comp/out_dec_rgb'

#prepare and clean up
mkdir -p py-motmetrics/res_dir_comp
rm data/experiment_uncompressed_result.csv

uuid=$(uuidgen) # unique identifier

class_arr=('ClassB' 'ClassC' 'ClassD' 'ClassE')
# class_arr=('ClassB') # for testing

qp=0 # actually not qp=0, but rather uncompressed
msr=0 # actually not msr=0, but rather uncompressed

for class_cat in ${class_arr[@]}
do
    if [ ${class_cat} == 'ClassB' ]
    then
        seq_name_arr=('BasketballDrive' 'Cactus' 'Kimono' 'ParkScene')
        resln='1920x1080'

        # test stage
        # seq_name_arr=('BasketballDrive')

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
            python3 detect.py\
                --source ${rgb_source_path}/${class_cat}/${seq_name}/\
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
                --img_path ${rgb_source_path}/${class_cat}/${seq_name}/\
                --max_age 1\
                --min_hits 5\
                --iou_threshold 0.4
            cd ..

            # clean up the result folder from py-motmetrics
            rm py-motmetrics/res_dir_comp/*.txt
            
            cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_comp/
            cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir/ # keep copy in res_dir
            
            ## evaluate the performance
            python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_comp/ > data/one_iter_${uuid}.txt

            # extracting values
            python3 experiment_tracker_format.py\
                --input_path data/one_iter_${uuid}.txt\
                --output_path data/experiment_uncompressed_result.csv\
                --class_cat ${class_cat}\
                --seq_name ${seq_name}\
                --class_id ${class_id}\
                --qp ${qp}\
                --msr ${msr}
        done
    done
done

rm data/one_iter_${uuid}.txt