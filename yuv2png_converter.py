import warnings
import numpy as np

import argparse
import re
import imageio
import os

from tqdm import tqdm

if __name__ == '__main__' :
  parser = argparse.ArgumentParser()

  parser.add_argument("--input"     ,      default = None)
  parser.add_argument("--resolution",      default = '832x480')
  parser.add_argument("--output_dir",      default = '.')

  args = parser.parse_args()

  file_name = args.input.split('/')[-1].split('.yuv')[0]

  splits = re.split(r'(\d+)', args.resolution)
  frm_width, frm_height = int(splits[1]), int(splits[3])

  file_size = os.path.getsize(args.input)
  frm_size  = int(frm_width * frm_height * 1.5) # YUV420
  num_frms = file_size // frm_size

  luma_size  = frm_width * frm_height
  chroma_size= frm_width * frm_height // 4

  with open(args.input, 'rb') as f:
    for i in tqdm(range(0, num_frms)):
      rawY = f.read(int(luma_size))
      rawY = np.frombuffer(rawY, dtype=np.uint8)
      rawY = rawY.reshape((frm_height, frm_width))

      rawU = f.read(int(chroma_size))
      rawU = np.frombuffer(rawU, dtype=np.uint8)
      rawU = rawU.reshape((frm_height//2, frm_width//2))

      rawV = f.read(int(chroma_size))
      rawV = np.frombuffer(rawV, dtype=np.uint8)
      rawV = rawV.reshape((frm_height//2, frm_width//2))

      planeY = rawY
      planeU = np.kron(rawU, np.ones([2, 2]))
      planeV = np.kron(rawV, np.ones([2, 2]))

      yuv444 = np.stack((planeY, planeU, planeV), axis=-1).astype('float32')

      y_offset = 16
      uv_offset = 128

      # according to ITU-R BT.709
      yuv444[:,:,0]  = yuv444[:,:, 0].astype(yuv444.dtype) - y_offset
      yuv444[:,:,1:] = yuv444[:,:,1:].astype(yuv444.dtype) - uv_offset
      A = np.array([[1.1689,  0.0000,  1.6023],
                    [1.1689, -0.3933, -0.8162],
                    [1.1689,  2.0251,  0.000]])

      # rgb
      rgb = np.round(np.dot(yuv444, A.T)).clip(0,255).astype('uint8')
      #bgr = rgb[:,:,::-1].copy()

      path = args.output_dir + "/" + file_name + '_seq_{:03}.png'.format(i)
      with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        imageio.imwrite(path, rgb)

