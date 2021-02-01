#!/bin/bash

echo "updating ground truth files starts ..."

if true
then
    echo "running commands ..."
    python3 obj_links.py SFU-HW-Objects-v1/class_b_BasketballDrive.txt >> class_b_BasketballDrive.log
    python3 obj_links.py SFU-HW-Objects-v1/class_b_BQTerrace.txt >> class_b_BQTerrace.log
    python3 obj_links.py SFU-HW-Objects-v1/class_b_Cactus.txt >> class_b_Cactus.log
    python3 obj_links.py SFU-HW-Objects-v1/class_b_Kimono.txt >> class_b_Kimono.log
    python3 obj_links.py SFU-HW-Objects-v1/class_b_ParkScene.txt >> class_b_ParkScene.log
    python3 obj_links.py SFU-HW-Objects-v1/class_c_BasketballDrill.txt >> class_c_BasketballDrill.log
    python3 obj_links.py SFU-HW-Objects-v1/class_c_BQMall.txt >> class_c_BQMall.log
    python3 obj_links.py SFU-HW-Objects-v1/class_c_PartyScene.txt >> class_c_PartyScene.log
    python3 obj_links.py SFU-HW-Objects-v1/class_c_RaceHorsesC.txt >> class_c_RaceHorsesC.log
    python3 obj_links.py SFU-HW-Objects-v1/class_d_BasketballPass.txt >> class_d_BasketballPass.log
    python3 obj_links.py SFU-HW-Objects-v1/class_d_BlowingBubbles.txt >> class_d_BlowingBubbles.log
    python3 obj_links.py SFU-HW-Objects-v1/class_d_BQSquare.txt >> class_d_BQSquare.log
    python3 obj_links.py SFU-HW-Objects-v1/class_d_RaceHorsesD.txt >> class_d_RaceHorsesD.log
else
   echo "Not running commands ... Set true in the bash script to run ..."
fi

echo "updating ground truth files ends ..."