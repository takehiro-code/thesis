rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
comp_source_path=/local-scratch/tta46/thesis/seq_comp

#cd yolov3
#rm output/${class_cat}/${seq_name}/labels/*.txt
#python3 detect.py\
#    --source ${rgb_source_path}/${class_cat}/${seq_name}/\
#    --weights weights/yolov3.pt\
#    --conf-thres 0.25\
#    --img-size 640\
#    --iou-thres 0.55\
#    --save-conf\
#    --save-txt\
#    --classes 0 41 58 74 77\
#    --project output/${class_cat}\
#    --name ${seq_name}\
#    --exist-ok
#cd ..

#conf=0.25
#iou=0.55
#img_s=640
#rm mAP/input/detection-results/*.txt
#rm mAP/input/ground-truth/*.txt
#python3 yolo2map.py\
#  --class_cat $class_cat\
#  --seq_name $seq_name\
#  --source_path $rgb_source_path >/dev/null 2>/dev/null
#
#cd mAP
#python3 main.py -na\
#  --class_cat ${class_cat}\
#  --seq_name ${seq_name}\
#  --conf_thres ${conf}\
#  --iou_thres ${iou}\
#  --img_size ${img_s}
#cd ..


#time bash optimize_detector.sh > data/log/tuning_detector_${class_cat}_${seq_name}.log
#time bash optimize_detector_v2.sh > data/log/tuning_detector_${class_cat}_${seq_name}_${class_id}_v2.log


class_cat=ClassC
seq_name=PartyScene
class_id="0"
time bash optimize_tracker.sh > data/log/tuning_tracker_${class_cat}_${seq_name}_${class_id}.log
