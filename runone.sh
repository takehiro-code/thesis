
echo "Run manual program ..."


#cp SFU-HW-Objects-v1/ClassB/Kimono/*.txt Org_Imgs_png/ClassB/Cactus
#rm class_b_Cactus.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_b_Cactus.txt | tee class_b_Cactus.log

#cp SFU-HW-Objects-v1/ClassB/Kimono/*.txt Org_Imgs_png/ClassB/Kimono
#rm class_b_Kimono.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_b_Kimono.txt | tee class_b_Kimono.log

#cp SFU-HW-Objects-v1/ClassC/RaceHorsesC/*.txt Org_Imgs_png/ClassC/RaceHorsesC
#rm class_c_RaceHorsesC.log
#mv ./Org_Imgs_png/ClassC/RaceHorsesC/* ./Yolo_mark/x64/Release/data/img
#readlink -e ./Yolo_mark/x64/Release/data/img/*.png > file_list.txt
#python3 obj_links_v2.py file_list.txt | tee class_c_RaceHorsesC.log
#mv ./Yolo_mark/x64/Release/data/img/* ./Org_Imgs_png/ClassC/RaceHorsesC

#cp SFU-HW-Objects-v1/ClassC/RaceHorsesC/*.txt Org_Imgs_png/ClassC/RaceHorsesC
#rm class_c_RaceHorsesC.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_c_RaceHorsesC.txt | tee class_c_RaceHorsesC.log

#cp SFU-HW-Objects-v1/ClassD/RaceHorsesD/*.txt Org_Imgs_png/ClassD/RaceHorsesD
#rm class_d_RaceHorsesD.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_d_RaceHorsesD.txt | tee class_d_RaceHorsesD.log

#cp SFU-HW-Objects-v1/ClassB/ParkScene/*.txt Org_Imgs_png/ClassB/ParkScene
#rm class_b_ParkScene.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_b_ParkScene.txt | tee class_b_ParkScene.log

#cp SFU-HW-Objects-v1/ClassC/PartyScene/*.txt Org_Imgs_png/ClassC/PartyScene
#rm class_c_PartyScene.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_c_PartyScene.txt | tee class_c_PartyScene.log

cp SFU-HW-Objects-v1/ClassD/BlowingBubbles/*.txt Org_Imgs_png/ClassD/BlowingBubbles
rm class_d_BlowingBubbles.log
python3 obj_links_v2.py SFU-HW-Objects-v1/class_d_BlowingBubbles.txt | tee class_d_BlowingBubbles.log

#cp SFU-HW-Objects-v1/ClassB/BasketballDrive/*.txt Org_Imgs_png/ClassB/BasketballDrive
#rm class_b_BasketballDrive.log
#python3 obj_links_v2.py SFU-HW-Objects-v1/class_b_BasketballDrive.txt | tee class_b_BasketballDrive.log


echo "manual program ends ..."