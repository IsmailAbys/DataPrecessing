from skimage.metrics import structural_similarity as ssim
import nibabel as nib
import numpy as np
import argparse



# @ray.remote
def ssim_(x,y):
    return ssim(x,y, data_range=(y.max()-y.min()))


# @ray.remote
def REshape(data):
    """
    Transform the 3D image to vector
    """
    return np.reshape(data, (data.shape[0]*data.shape[1]*data.shape[2], ))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SSIM mesure between two images')
    parser.add_argument("-image1",  type=str, required=True, help="path to input image1")    
    parser.add_argument("-image2", type=str, required=True, help="path to input image2")    
    args = parser.parse_args()
    image1 = nib.load(args.image1).get_fdata()
    image2 = nib.load(args.image2).get_fdata()

    if image1.shape != image2.shape :
        raise ValueError("The images must have the same dimension")
    image1_vec_id = REshape(image1)
    image2_vec_id = REshape(image2)
    ssim_value = ssim_(image1_vec_id, image2_vec_id)
    print(f"ssim between image1 and image2: {ssim_value}")
