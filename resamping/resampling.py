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


# compute the scale foctor of each image
def scale_factor(data, x, y, z):
    
    scale_factors = []
    for i in range(len(data)):

        x_sc_f = x/ data[i].shape[0]
        y_sc_f = y/ data[i].shape[1]
        z_sc_f = z/ data[i].shape[2]


 
        scale_factor = [x_sc_f, y_sc_f, z_sc_f]
        scale_factors.append(scale_factor)
        return scale_factors


# downsampling
def resampling(data, scale_factors):
    """
    This function takes two parameters as input:
        data: This parameter represents the input data, which can be a list of images or a single image.
        This is the ratio of the new dimension to the old dimension (dimension of the input image).
    """
    zoom_factors = []
    data_list = []
    for i in range(len(data)):
        scale_factors = np.asarray(scale_factors)
        new_shape = data[i].shape * scale_factors[i]
        new_shape = np.round(new_shape)
        
        zoom_factor = new_shape / data[i].shape
        zoom_factors.append(zoom_factor)
    
        data_ = scipy.ndimage.zoom(data[i], zoom_factors[i], order=1, prefilter=True) 
        data_list.append(data_)
    return data_list





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The resampling the data')
    # parser.add_argument("--img", type=str, required=True, help="path to input image") # If you need to resample only one image, use this command
    parser.add_argument('--data-dir', type=str, help='path of the input data') # If you have a database to resample, you need to use this command
    parser.add_argument("--out-dir", type=str, help="path to output image")   # This command allows you to save the outputs the selected directory.              
    parser.add_argument('-x', type=int, default=512, help='size of x') # By default the size of x is 512, you can change using this comnad -x
    parser.add_argument('-y', type=int, default=512, help='size of y') # By default the size of y is 512, you can change using this comnad -y
    parser.add_argument('-z', type=int, default=500,help='size of z') # By default the size of z is 512 in this because it is the mean of the database of TotalSeg, you can change using this comnad -z
    args = parser.parse_args()
    images = sorted(glob.glob(os.path.join(args.data_dir, "*.nii.gz"))) # Selecting the path of the input data.
    data = list(MyDataset(images))
    scale_factors = scale_factor(data, args.x, args.y, args.z)
    resampled_data = resampling(data, scale_factors)
    idx = 0
    for item in resampled_data:
        nii = nib.Nifti1Image(item, np.eye(4))
        nib.save(nii, os.path.join(args.out_dir, f"resampled_image_{idx}.nii.gz")) # Saving the outputs in the selected directory.
        idx += 1


