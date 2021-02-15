
class_cat=ClassB
seq_name=BasketballDrive
class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
comp_source_path=/local-scratch/tta46/thesis/seq_comp

rm data/tuning_detector_result_${class_cat}_${seq_name}_v2.csv
rm py-motmetrics/res_dir_opt/*.txt
mkdir -p py-motmetrics/res_dir_opt

# detector parameters
declare -a conf_thres=($(seq 0.1 0.05 0.9))
declare -a iou_thres=($(seq 0.1 0.05 0.9))
#declare -a img_size=($(seq 200 20 900))
declare -a img_size=(640)


# tracker parameters (default)
maxa=1
minh=3
iou_track=0.3

# unique id for one_iter.txt dump file 
uuid=$(uuidgen)

for conf in ${conf_thres[@]}
do
  for iou in ${iou_thres[@]}
  do
    for img_s in ${img_size[@]}
    do
      # detecting
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
          --classes 0 32 56\
          --project output/${class_cat}\
          --name ${seq_name}\
          --exist-ok >/dev/null 2>/dev/null
      cd ..

      # conversion
      python3 yolo2mot.py\
         --class_cat ${class_cat}\
         --seq_name ${seq_name}\
         --class_id ${class_id}\
         --source_path ${rgb_source_path}\

      # tracking
      echo "Running tracker for max_age=${maxa}, min_hits=${minh}, iou_thres=${iou_track}"
      cd sort
      python3 sort.py\
         --seq_path input/${class_cat}_${seq_name}_${class_id}\
         --img_path ${rgb_source_path}/${class_cat}/${seq_name}\
         --max_age ${maxa}\
         --min_hits ${minh}\
         --iou_threshold ${iou_track}
      cd ..
     
      # copying tracking result to metrics evaluation place
      cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_opt/
      
      ## evaluate the performance
      python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_opt/ > data/one_iter_${uuid}.txt
      
      # extracting values
      python3 optimize_detector_format.py\
        --input_path data/one_iter_${uuid}.txt\
        --output_path data/tuning_detector_result_${class_cat}_${seq_name}_v2.csv\
        --conf_thres ${conf}\
        --iou_thres ${iou}\
        --img_size ${img_s}
    done
  done
done

# clean up
rm data/one_iter_${uuid}.txt

