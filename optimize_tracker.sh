
class_cat=ClassC
seq_name=PartyScene
class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
comp_source_path=/local-scratch/tta46/thesis/seq_comp

rm data/tuning_tracker_result_${class_cat}_${seq_name}.csv
rm data/one_iter.txt
#rm py-motmetrics/res_dir_opt/*.txt
mkdir -p py-motmetrics/res_dir_opt

conf=0.2
iou_detect=0.35
img_s=640

# first generates the yolo v3 output
echo "Running detector for conf_thres=${conf}, iou_thres=${iou}, img_size=${img_s}"
cd yolov3
rm output/${class_cat}/${seq_name}/labels/*.txt
python3 detect.py\
    --source ${rgb_source_path}/${class_cat}/${seq_name}/\
    --weights weights/yolov3.pt\
    --conf ${conf}\
    --img-size ${img_s}\
    --iou-thres ${iou_detect}\
    --save-txt\
    --classes 0 41 58 74 77\
    --project output/${class_cat}\
    --name ${seq_name}\
    --exist-ok >/dev/null 2>/dev/null
cd ..

python3 yolo2mot.py\
   --class_cat ${class_cat}\
   --seq_name ${seq_name}\
   --class_id ${class_id}\
   --source_path ${rgb_source_path}\

# grid search on tracker
declare -a max_age=($(seq 1 1 9))
declare -a min_hits=($(seq 1 1 9))
declare -a iou_thres=($(seq 0.1 0.05 0.9))

for maxa in ${max_age[@]}
do
  for minh in ${min_hits[@]}
  do
    for iou_track in ${iou_thres[@]}
    do
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
      python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_opt/ > data/one_iter.txt
      
      # extracting values
      python3 optimize_tracker_formating.py\
        --input_path data/one_iter.txt\
        --output_path data/tuning_tracker_result_${class_cat}_${seq_name}.csv\
        --max_age ${maxa}\
        --min_hits ${minh}\
        --iou_thres ${iou_track}

    done
  done
done




