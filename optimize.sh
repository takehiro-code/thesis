
class_cat=ClassC
seq_name=PartyScene
#class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/workspace/seq_test
comp_source_path=/local-scratch/tta46/workspace/seq_comp


rm data/tuning_detector_result.txt

declare -a img_size=($(seq 200 20 1000))
#declare -a img_size=(640)
for value in ${img_size[@]}
do
  echo "Running for conf_thres=0.25, iou_thres=0.45, img_size=${value}"
  cd yolov3
  rm output/${class_cat}/${seq_name}/labels/*.txt
  python3 detect.py\
      --source ${rgb_source_path}/${class_cat}/${seq_name}/\
      --weights weights/yolov3.pt\
      --conf 0.25\
      --img-size ${value}\
      --iou-thres 0.45\
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
    --conf_thres 0.25\
    --iou_thres 0.45\
    --img_size $value
  cd ..

done

python3 grid_search.py\
  --input_path data/tuning_detector_result.txt





