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
    data = nib.load('D:\\sujetFracTest\\image.nii.gz').get_fdata()
    data_vec = reshaping(data)
    plot_hist(data_vec)