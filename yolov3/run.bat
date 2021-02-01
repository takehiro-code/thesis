
echo "run yolov3 program ..."

@REM rem --------------------------------------------------------------------------------------------
@REM rem Class B
@REM rem --------------------------------------------------------------------------------------------

@REM del output\ClassB\BasketballDrive\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassB/BasketballDrive/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 32 56^
@REM     --project output/ClassB^
@REM     --name BasketballDrive^
@REM     --exist-ok

@REM del output\ClassB\Cactus\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassB/Cactus/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --save-img^
@REM     --classes 58^
@REM     --project output/ClassB^
@REM     --name Cactus^
@REM     --exist-ok

@REM del output\ClassB\Kimono\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassB/Kimono/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 26^
@REM     --project output/ClassB^
@REM     --name Kimono^
@REM     --exist-ok

@REM del output\ClassB\ParkScene\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassB/ParkScene/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 1 13^
@REM     --project output/ClassB^
@REM     --name ParkScene^
@REM     --exist-ok


@REM @REM --------------------------------------------------------------------------------------------
@REM @REM Class C
@REM @REM --------------------------------------------------------------------------------------------

@REM del output\ClassC\BasketballDrill\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassC/BasketballDrill/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 32 56^
@REM     --project output/ClassC^
@REM     --name BasketballDrill^
@REM     --exist-ok

@REM del output\ClassC\PartyScene\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassC/PartyScene/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 41 58 74 77^
@REM     --project output/ClassC^
@REM     --name PartyScene^
@REM     --exist-ok

@REM del output\ClassC\RaceHorsesC\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassC/RaceHorsesC/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 17^
@REM     --project output/ClassC^
@REM     --name RaceHorsesC^
@REM     --exist-ok


@REM @REM --------------------------------------------------------------------------------------------
@REM @REM Class D
@REM @REM --------------------------------------------------------------------------------------------

@REM del output\ClassD\BasketballPass\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassD/BasketballPass/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 32 56^
@REM     --project output/ClassD^
@REM     --name BasketballPass^
@REM     --exist-ok

@REM del output\ClassD\BlowingBubbles\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassD/BlowingBubbles/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 41 77^
@REM     --project output/ClassD^
@REM     --name BlowingBubbles^
@REM     --exist-ok

@REM del output\ClassD\RaceHorsesD\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassD/RaceHorsesD/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 17^
@REM     --project output/ClassD^
@REM     --name RaceHorsesD^
@REM     --exist-ok

@REM @REM --------------------------------------------------------------------------------------------
@REM @REM Class E
@REM @REM --------------------------------------------------------------------------------------------

@REM del output\ClassE\FourPeople\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassE/FourPeople/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 41 56 58^
@REM     --project output/ClassE^
@REM     --name FourPeople^
@REM     --exist-ok

@REM del output\ClassE\Johnny\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassE/Johnny/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 27 63^
@REM     --project output/ClassE^
@REM     --name Johnny^
@REM     --exist-ok

@REM del output\ClassE\KristenAndSara\labels\*.txt
@REM python detect.py^
@REM     --source ../Org_Imgs_png/ClassE/KristenAndSara/*.png^
@REM     --weights weights/yolov3.pt^
@REM     --conf 0.50^
@REM     --save-txt^
@REM     --classes 0 63 67^
@REM     --project output/ClassE^
@REM     --name KristenAndSara^
@REM     --exist-ok


echo "yolov3 program ends ..."
