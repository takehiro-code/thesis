
# inputs
class_cat=ClassC
seq_name=PartyScene
class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/workspace/seq_test
comp_source_path=/local-scratch/tta46/workspace/seq_comp
test_flag=false

if ${test_flag} == true
then
  class_cat=Class_test
  seq_name="TUD-Stadtmitte"
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
      --conf 0.50\
      --save-txt\
      --classes ${class_id}\
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
     --img_path ${rgb_source_path}/${class_cat}/${seq_name}
 cd ..

 mkdir py-motmetrics/res_dir_exp

 cp sort/output/${class_cat}_${seq_name}_${class_id}.txt py-motmetrics/res_dir_exp/

 ## evaluate the performance
 python3 py-motmetrics/motmetrics/apps/eval_motchallenge.py py-motmetrics/gt_dir/ py-motmetrics/res_dir_exp/

# ------------------------------------------------------------------------------------
# compression
# ------------------------------------------------------------------------------------
#qp=22
#yuv_input_path=${yuv_source_path}/${class_cat}/${seq_name}_1920x1080_50.yuv
##name='BasketballDrive'
##out='qp'${qp}'_ClassB_'${seq_name}
#out=${class_cat}_${seq_name}_qp${qp}
#
#cd video_comp
#./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${seq_ame}.cfg -i ${yuv_input_path} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_${out}.txt
#./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt
#cd ..
#


#qp=22
#seq=${yuv_source_path}/ClassB/BasketballDrive_1920x1080_50.yuv
#name='BasketballDrive'
#out='qp'${qp}'_classB_'${name}
#cd video_comp
#./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_${out}.txt
#./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt
#cd ..

#python3 yuv2png_converter.py\
#  --input video_comp/out_dec/rec_qp22_classB_BasketballDrive.yuv\
#  --resolution 1920x1080 --output_dir seq_comp/ClassB/BasketballDrive
  echo "actual experiment"

fi
