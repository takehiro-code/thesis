
class_cat=ClassD
seq_name=BasketballPass
class_id="56"
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
out_dec_rgb_path='/local-scratch/tta46/thesis/video_comp/out_dec_rgb'

#color conversion
#yuv_name="BasketballPass_416x240_50.yuv"
#resln="416x240"
#cd video_comp
#rm out_dec_rgb/*.png
#sleep 2
#python3 yuv2png_converter.py\
#    --input ${yuv_source_path}/${class_cat}/${yuv_name}\
#    --resolution ${resln}\
#    --output_dir out_dec_rgb
#sleep 2
#cd ..


# cd yolov3
# rm output/${class_cat}/${seq_name}/labels/*.txt
# python3 detect.py\
#     --source ${out_dec_rgb_path}/\
#     --weights weights/yolov3.pt\
#     --conf-thres 0.25\
#     --img-size 640\
#     --iou-thres 0.55\
#     --save-conf\
#     --save-txt\
#     --classes ${class_id}\
#     --project output/${class_cat}\
#     --name ${seq_name}\
#     --exist-ok
# cd ..

conf=0.25
iou=0.55
img_s=640
rm mAP/input/detection-results/*.txt
rm mAP/input/ground-truth/*.txt
python3 yolo2map.py\
  --class_cat $class_cat\
  --seq_name $seq_name\
  --class_id ${class_id}\
  --source_path $out_dec_rgb_path # >/dev/null 2>/dev/null

cd mAP
python3 main.py -na\
  --class_cat ${class_cat}\
  --seq_name ${seq_name}\
  --class_id ${class_id}\
  --conf_thres ${conf}\
  --iou_thres ${iou}\
  --img_size ${img_s}
cd ..

