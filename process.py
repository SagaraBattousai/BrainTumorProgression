import sys
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from typing import Sequence, Tuple, Union
import ast
import csv

import numpy as np
import SimpleITK as sitk
import pythonal
import ganondorf.data.format_image_data as fid

def load_image_array(filename: str) -> np.array:
  return sitk.GetArrayFromImage(sitk.ReadImage(filename))

def save_image_array(image: np.array, filename: str = "output.nii.gz") -> None:
  sitk.WriteImage(sitk.GetImageFromArray(image), filename)

def remove_slides(image: np.array, slides: Sequence, axis: int = 0) -> np.array:
  pass

def remove_surplus_slides(metadata_file: str = 'supplementary.csv',
                          axis: int = 0) -> None:
  pre_scan_name  = "Pre_Scan_T1.nii.gz"
  pre_mask_name  = "Pre_Mask.nii.gz"
  post_scan_name = "Post_Scan_T1.nii.gz"
  post_mask_name = "Post_Mask.nii.gz"

  meta = open(metadata_file, newline='')
  reader = csv.DictReader(meta, escapechar='\\')
  slides = {row['id'] : ast.literal_eval(row[' slices_removed'].strip()) \
            for row in reader}

  for key in slides:
    pre_removal  = list(map(lambda a: a - 1, slides[key][0]))
    post_removal = list(map(lambda a: a - 1, slides[key][1]))

    pre_scan_path  = os.path.join(key, pre_scan_name)
    pre_mask_path  = os.path.join(key, pre_mask_name)
    post_scan_path = os.path.join(key, post_scan_name)
    post_mask_path = os.path.join(key, post_mask_name)

    pre_arr = np.delete(load_image_array(pre_scan_path), pre_removal, axis)
    pre_msk = np.delete(load_image_array(pre_mask_path), pre_removal, axis)

    post_arr = np.delete(load_image_array(post_scan_path), post_removal, axis)
    post_msk = np.delete(load_image_array(post_mask_path), post_removal, axis)

    save_image_array(pre_arr, pre_scan_path)
    save_image_array(pre_msk, pre_mask_path)

    save_image_array(post_arr, post_scan_path)
    save_image_array(post_msk, post_mask_path)

#######################

def pad_slides_depth(final_depth_size: int = 24,
                     axis: int = 0,
                     pad_value: Union[int, float] = 0,
                     dir_range: Tuple[int,int] = (1, 12),
                     image_types: int = 4) -> None:
  

  dir_count = dir_range[1] - dir_range[0]

  image_names  = ["Pre_Scan_T1.nii.gz",
                  "Pre_Mask.nii.gz",
                  "Post_Scan_T1.nii.gz",
                  "Post_Mask.nii.gz"] * dir_count

  dirs = ['{:02}'.format(i) for i in range(*dir_range)] * image_types

  dirs.sort()

  for path in pythonal.zipwith(os.path.join, dirs, image_names):
    image = load_image_array(path)
    depth_increase = final_depth_size - image.shape[0]
    
    if depth_increase < 1:
      continue

    if pad_value == 0:
      pad = np.zeros((depth_increase, *image.shape[1:]))
    else:
      pad = np.ones((depth_increase, *image.shape[1:])) * pad_value

    padded_image = np.concatenate((image, pad), axis=axis)

    save_image_array(padded_image, path)




def fix_aspect_ratio(img_name):
  img = sitk.GetArrayFromImage(sitk.ReadImage(img_name))
  arrs = [arr for arr in img]
  h, w = arrs[0].shape
  (left, right, top, bottom) = (0,0,0,0)

  if h > w:
    diff = h - w
    left = diff // 2
    right = diff - left
  elif h < w:
    diff = w - h
    top = diff // 2
    bottom = diff - top
  else:
    return img

  out_arrs = [np.pad(arr, ((top, bottom), (left,right)), constant_values=0) \
              for arr in arrs]

  out_array = np.stack(out_arrs, 0)

  return sitk.GetImageFromArray(out_array)

if __name__ == '__main__':
  # if len(sys.argv) > 1:
  #   fid.convert_dir_images_to_nii(sys.argv[1])
  # else:
  #   fid.convert_dir_images_to_nii()

  for root, dirnames, fnames in os.walk('.'):
    if dirnames != []:
      continue

    if next(filter(lambda filename: filename.endswith(".dcm"), fnames), False):

      print(root)

    fid.convert_dir_images_to_nii(outname=f'{root}/out.nii', dirname=root)




