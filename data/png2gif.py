# this script will generate the gif (or other format if you'd like) in a specified frames.

import imageio
import os
import re
import pdb

# input folder and output video file path can be entered here:
image_folder = 'vid/ClassD_BasketballPass_0_uncomp'
video_name = 'ClassD_BasketballPass_0_uncomp.gif'

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = natural_sort(images)

num_frames = 0

with imageio.get_writer(video_name, mode='I', fps=10) as writer:
    for filename in images:
        if num_frames  > 40  and num_frames < 127:
            image = imageio.imread(f"{image_folder}/{filename}")
            image_cropped = image[0:286, 20:496] # sliced the width by 20px
            writer.append_data(image_cropped)
        num_frames += 1