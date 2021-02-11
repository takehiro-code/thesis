src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'

#Class B
#BasketballDirve
qp=22
seq='ClassB/BasketballDrive_1920x1080_50.yuv'
name='BasketballDrive'
out='qp'${qp}'_classB_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt


#BQTerrace
qp=22
seq='ClassB/BQTerrace_1920x1080_60.yuv'
name='BQTerrace'
out='qp'${qp}'_classB_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#Cactus
qp=22
seq='ClassB/Cactus_1920x1080_50.yuv'
name='Cactus'
out='qp'${qp}'_classB_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#ParkScene
qp=22
seq='ClassB/ParkScene_1920x1080_24.yuv'
name='ParkScene'
out='qp'${qp}'_classB_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#Kimono
qp=22
seq='ClassB/Kimono1_1920x1080_24.yuv'
name='Kimono'
out='qp'${qp}'_classB_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt


#Class C
#BasketballDrill
qp=22
seq='ClassC/BasketballDrill_832x480_50.yuv'
name='BasketballDrill'
out='qp'${qp}'_classC_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#BQMall
qp=22
seq='ClassC/BQMall_832x480_60.yuv'
name='BQMall'
out='qp'${qp}'_classC_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#PartyScene
qp=22
seq='ClassC/PartyScene_832x480_50.yuv'
name='PartyScene'
out='qp'${qp}'_classC_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#RaceHorsesC
qp=22
seq='ClassC/RaceHorses_832x480_30.yuv'
name='RaceHorsesC'
out='qp'${qp}'_classC_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt


#Class D
#BasketballPass
qp=22
seq='ClassD/BasketballPass_416x240_50.yuv'
name='BasketballPass'
out='qp'${qp}'_classD_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#BlowingBubbles
qp=22
seq='ClassD/BlowingBubbles_416x240_50.yuv'
name='BlowingBubbles'
out='qp'${qp}'_classD_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#BQSquare
qp=22
seq='ClassD/BQSquare_416x240_60.yuv'
name='BQSquare'
out='qp'${qp}'_classD_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#RaceHorses
qp=22
seq='ClassD/RaceHorses_416x240_30.yuv'
name='RaceHorses'
out='qp'${qp}'_classD_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt


#Class E 
#FourPeople
qp=22
seq='ClassE/FourPeople_1280x720_60.yuv'
name='FourPeople'
out='qp'${qp}'_classE_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#Johnny
qp=22
seq='ClassE/Johnny_1280x720_60.yuv'
name='Johnny'
out='qp'${qp}'_classE_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

#KristenAndSara
qp=22
seq='ClassE/KristenAndSara_1280x720_60.yuv'
name='KristenAndSara'
out='qp'${qp}'_classE_'${name}
./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt
./TAppDecoderStatic -b out_bin/${out}.bin -o out_dec/rec_${out}.yuv | tee out_log/log_${out}.txt

