import os
import torch
import glob
import argparse
import numpy as np
import scipy.ndimage
import nibabel as nib

from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, path):
        # load all nii handle in a list
        self.images_list = [nib.load(image_path) for image_path in path]
    
    def __len__(self):
        return len(self.images_list)

    def __getitem__(self, idx):
        nii_image = self.images_list[idx]
        data = np.asarray(nii_image.dataobj)
        return data


if __name__ == "__main__":      
    parser = argparse.ArgumentParser(description='Data cropping')
    parser.add_argument("-i", '--data-dir', type=str, help='path of the input data')
    parser.add_argument("-o", '--out-dir', type=str, help='path to the cropped data')
    args = parser.parse_args()
    idx = 0
    images_path = sorted(glob.glob(os.path.join(args.data_dir,  "*.nii.gz")))

    input_data = MyDataset(images_path)
    for item, path in zip(input_data, images_path):
        file_name = os.path.basename(path)
        rows, cols, slices = np.where(item != 0)
        after_cropped= item[rows.min():rows.max() + 1,cols.min():cols.max() + 1,slices.min():slices.max() + 1]
        print(f"intial shape : {item.shape} ---> the shape after cropped : {after_cropped.shape}")
        nii = nib.Nifti1Image(after_cropped, np.eye(4))
        nib.save(nii, os.path.join(args.out_dir, file_name))
        idx += 1


