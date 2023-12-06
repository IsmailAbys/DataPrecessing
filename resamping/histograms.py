import os
import argparse
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


# Reshape 3D tensor to a vector 
def reshaping(x):
    return np.reshape(x, (x.shape[0]*x.shape[1]*x.shape[2],))


# plot histogram
def plot_hist(x):
    plt.figure(figsize=(10, 10))
    plt.hist(x, histtype='bar')
    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The resampling the data')
    parser.add_argument("-i", "--input", type=str, required=True, help="path to input image") # If you need to resample only one image, use this command
    args = parser.parse_args()
    data_vec = reshaping(nib.load(args.input).get_fdata())
    plot_hist(data_vec)