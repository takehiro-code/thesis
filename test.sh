
class_cat=ClassC
seq_name=PartyScene
#class_id=0
rgb_source_path=/local-scratch/share_dataset/labled_hevc_sequences
yuv_source_path=/local-scratch/chyomin/HEVC_Common_Test_Sequence
test_source_path=/local-scratch/tta46/workspace/seq_test
comp_source_path=/local-scratch/tta46/workspace/seq_comp

cd yolov3
rm output/${class_cat}/${seq_name}/labels/*.txt
python3 detect.py\
    --source ${rgb_source_path}/${class_cat}/${seq_name}/\
    --weights weights/yolov3.pt\
    --conf 0.25\
    --img-size 640\
    --iou-thres 0.45\
    --save-txt\
    --classes 0 41 58 74 77\
    --project output/${class_cat}\
    --name ${seq_name}\
    --exist-ok
cd ..