import cv2
import os
import re
import pdb

image_folder = 'vid'
video_name = 'ClassD_BasketballPass_0.avi'

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)


images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = natural_sort(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, fps=30, frameSize=(width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()