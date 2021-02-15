
class_cat=ClassC
seq_name=PartyScene
class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
comp_source_path=/local-scratch/tta46/thesis/seq_comp

rm data/tuning_detector_result_${class_cat}_${seq_name}.csv

declare -a conf_thres=($(seq 0.1 0.05 0.9))
declare -a iou_thres=($(seq 0.1 0.05 0.9))
#declare -a img_size=($(seq 200 20 900))
declare -a img_size=(640)
for conf in ${conf_thres[@]}
do
  for iou in ${iou_thres[@]}
  do
    for img_s in ${img_size[@]}
    do
      echo "Running detector for conf_thres=${conf}, iou_thres=${iou}, img_size=${img_s}"
      cd yolov3
      rm output/${class_cat}/${seq_name}/labels/*.txt
      python3 detect.py\
          --source ${rgb_source_path}/${class_cat}/${seq_name}/\
          --weights weights/yolov3.pt\
          --conf ${conf}\
          --img-size ${img_s}\
          --iou-thres ${iou}\
          --save-txt\
          --classes 0 41 58 74 77\
          --project output/${class_cat}\
          --name ${seq_name}\
          --exist-ok >/dev/null 2>/dev/null
      cd ..
    
      rm mAP/input/detection-results/*.txt
      rm mAP/input/ground-truth/*.txt
      python3 yolo2map.py\
        --class_cat $class_cat\
        --seq_name $seq_name\
        --source_path $rgb_source_path >/dev/null 2>/dev/null
    
      cd mAP
      python3 main.py -na -np -q\
        --class_cat ${class_cat}\
        --seq_name ${seq_name}\
        --conf_thres ${conf}\
        --iou_thres ${iou}\
        --img_size ${img_s}
      cd ..
    done
  done
done


#python3 grid_search.py\
#  --input_path data/tuning_detector_result_${class_cat}_${seq_name}.csv





