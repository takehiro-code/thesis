
# inputs
class_cat=ClassC
seq_name=PartyScene
class_id="all"
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
comp_source_path=/local-scratch/tta46/thesis/seq_comp
test_flag=false

if ${test_flag} == true
then
  class_cat=Class_test
  seq_name="ADL-Rundle-8"
  class_id=0
  
  cd yolov3
  rm output/${class_cat}/${seq_name}/labels/*.txt
  python3 detect.py\
      --source ${test_source_path}/${class_cat}/${seq_name}/\
      --weights weights/yolov3.pt\
      --conf 0.25\
      --save-txt\
      --classes ${class_id}\
      --project output/${class_cat}\
      --name ${seq_name}\
      --exist-ok
  cd ..

  python3 yolo2mot.py\
     --class_cat ${class_cat}\
     --seq_name ${seq_name}\
     --class_id ${class_id}\
     --source_path ${test_source_path}\
     --test
     
  cd sort
  python3 sort.py\
     --seq_path input/${class_cat}_${seq_name}_${class_id}\
     --img_path ..${test_source_path}/${class_cat}/${seq_name}
  cd ..
  
  mkdir py-motmetrics/res_dir_exp
  
  cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_exp/
  
  ## evaluate the performance
  python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_exp/

else

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
      --classes 0 41 58 74 77\
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
     --img_path ${rgb_source_path}/${class_cat}/${seq_name}\
     --max_age 1\
     --min_hits 5\
     --iou_threshold 0.4
  cd ..
  
  mkdir -p py-motmetrics/res_dir_exp
  
  cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_exp/
  
  ## evaluate the performance
  python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_exp/

fi
