# only one run of the experiment, for testing purpose
class_cat=ClassE
seq_name=FourPeople
class_id="all"
if [ ${class_id} == "all" ]
then
    # class_id_arr=(0 41 58 74 77) # for PartyScene
    # class_id_arr=(0 32 56) # BasketballPass
    # class_id_arr=(0 41 77) # BlowingBubbles
    # class_id_arr=(0 17) # RaceHorsesC
    # class_id_arr=(0 27 63) # Johnny
    class_id_arr=(0 41 56 58) # FourPeople
else
    class_id_arr=(${class_id})
fi
qp=18
msr=16
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/thesis/seq_test
out_dec_rgb_path='/local-scratch/tta46/thesis/video_comp/out_dec_rgb'
output_path="data/test_output.csv"

rm ${output_path}
uuid=$(uuidgen) # unique identifier

#color conversion
# yuv_name="FourPeople_1280x720_60.yuv"
# resln="1280x720"
# cd video_comp
# rm out_dec_rgb/*.png
# sleep 2
# python3 yuv2png_converter.py\
#    --input ${yuv_source_path}/${class_cat}/${yuv_name}\
#    --resolution ${resln}\
#    --output_dir out_dec_rgb
# sleep 2
# cd ..

#run yolov3 detector, output the det results
cd yolov3
rm output/${class_cat}/${seq_name}/labels/*.txt
python3 detect.py\
    --source ${out_dec_rgb_path}/\
    --weights weights/yolov3.pt\
    --conf-thres 0.25\
    --img-size 640\
    --iou-thres 0.55\
    --save-conf\
    --classes ${class_id_arr[@]}\
    --save-txt\
    --project output/${class_cat}\
    --name ${seq_name}\
    --exist-ok
cd ..

# copying the det results to the folder for backup
mkdir -p data/det_results/${class_cat}_${seq_name}_${class_id}_qp${qp}_msr${msr}
rm data/det_results/${class_cat}_${seq_name}_${class_id}_qp${qp}_msr${msr}/*.txt
sleep 2
cp yolov3/output/${class_cat}/${seq_name}/labels/*.txt data/det_results/${class_cat}_${seq_name}_${class_id}_qp${qp}_msr${msr}
sleep 2

## convert to YOLO format to PASCAL VOC format for mAP measurement
conf=0.25
iou=0.55
img_s=640
rm mAP/input/detection-results/*.txt
rm mAP/input/ground-truth/*.txt
python3 -W ignore yolo2map.py\
  --class_cat $class_cat\
  --seq_name $seq_name\
  --class_id ${class_id}\
  --source_path $out_dec_rgb_path

cd mAP
mAP=`python3 main.py -na -np -q\
  --class_cat ${class_cat}\
  --seq_name ${seq_name}\
  --class_id ${class_id}\
  --conf_thres ${conf}\
  --iou_thres ${iou}\
  --img_size ${img_s}`
cd ..

python3 -W ignore yolo2mot.py\
    --class_cat ${class_cat}\
    --seq_name ${seq_name}\
    --class_id ${class_id}\
    --source_path ${out_dec_rgb_path}
sleep 2

cd sort
python3 sort.py\
    --seq_path input/${class_cat}_${seq_name}_${class_id}\
    --img_path ${out_dec_rgb_path}\
    --max_age 1\
    --min_hits 5\
    --iou_threshold 0.4
sleep 2
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

echo "mAP = ${mAP}"
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

rm data/one_iter_${uuid}.txt
