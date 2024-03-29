src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'

class='ClassC'
seq="${src_addr}/${class}/RaceHorses_832x480_30.yuv"
name='RaceHorsesC'

#qp_arr=(18 22 26 30 34 38)
#msr=(16 32 64)

qp_arr=(6 10 14 18 22 26 30 34 38 42 46)
msr_arr=(8 16 32 48 64 80 96)

for qp in ${qp_arr[@]}
do
  for msr in ${msr_arr[@]}
  do
    echo "encoding ${class} ${name} at qp=${qp}, mer=${msr}"
    out=${class}_${name}_qp${qp}_msr${msr}
    ./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -sr ${msr} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt

  done
done