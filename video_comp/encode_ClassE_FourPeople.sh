src_addr='/local-scratch/chyomin/HEVC_Common_Test_Sequence'

class='ClassE'
seq="${src_addr}/${class}/FourPeople_1280x720_60.yuv"
name='FourPeople'

declare -a qp_arr=(18 22 26 30 34 38)
declare -a msr_arr=(16 32 64)

for qp in ${qp_arr[@]}
do
  for msr in ${msr_arr[@]}
  do
    echo "encoding ${class} ${name} at qp=${qp}, mer=${msr}"
    out=${class}_${name}_qp${qp}_msr${msr}
    ./TAppEncoderStatic -c encoder_lowdelay_P_main.cfg -c ./per-sequence/${name}.cfg -i ${seq} -q ${qp} -sr ${msr} -b out_bin/${out}.bin | tee out_log/log_enc_${out}.txt

  done
done