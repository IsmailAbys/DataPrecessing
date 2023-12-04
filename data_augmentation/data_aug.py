import nibabel as nib
import os
import numpy as np
from scipy.ndimage import affine_transform
import time
import argparse


start = time.time()


class Data_aug(object):
    
    def brightness(X):
        """
        Changing the brighness of a image using power-law gamma transformation.
        Gain and gamma are chosen randomly for each image channel.
    
        Gain chosen between [1.2 - 2.0]
        Gamma chosen between [1.2 - 2.0]
    
        new_im = gain * im^gamma
        """
        X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
        X_new = np.zeros(X.shape)

        for c in range(X.shape[-1]):
            im = X[:,:,:, c]        
            gain =0.67474081005230144
            gamma = 1.1
            im_new = np.sign(im)*gain*(np.abs(im)**gamma)
            X_new[:,:,:, c] = im_new 
        X_new = np.reshape(X_new, (X_new.shape[0], X_new.shape[1], X_new.shape[2]))
        nii = nib.Nifti1Image(X_new, np.eye(4))
        return nii


    def flip3D(X):
        """
        Flip the 3D image respect one of the 3 axis chosen randomly

        To choose the axis of flipping, (for example z) you need only this axis.
        """
        choice = np.random.randint(3)
        if choice == 0: # flip on x
            X_flip = X[::-1, :, :]
        if choice == 1: # flip on y
            X_flip = X[:, ::-1, :]
        if choice == 2: # flip on z
            X_flip= X[:, :, ::-1]
        return nib.Nifti1Image(X_flip, np.eye(4))


    def rotation_zoom3D(X):
        """
        Rotate a 3D image with alfa, beta and gamma degree respect the axis x, y and z respectively.
            The three angles are chosen randomly between 0-30 degrees
        """
        alpha, beta, gamma = np.random.random_sample(3)*np.pi/10
        Rx = np.array([[1, 0, 0],
                    [0, np.cos(alpha), -np.sin(alpha)],
                    [0, np.sin(alpha), np.cos(alpha)]])
    
        Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                    [0, 1, 0],
                    [-np.sin(beta), 0, np.cos(beta)]])
    
        Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                    [np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])
        
        R_rot = np.dot(np.dot(Rx, Ry), Rz)
        
        a, b = 0.8, 1.2
        alpha, beta, gamma = (b-a)*np.random.random_sample(3) + a
        R_scale = np.array([[alpha, 0, 0],
                    [0, beta, 0],
                    [0, 0, gamma]])
        
        R = np.dot(R_rot, R_scale)
        X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
        X_rot = np.empty_like(X)
        for channel in range(X.shape[-1]):
            X_rot[:,:,:,channel] = affine_transform(X[:,:,:,channel], R, offset=0, order=1, mode='constant')
        X_rot = np.reshape(X_rot, (X_rot.shape[0], X_rot.shape[1], X_rot.shape[2]))
        nii = nib.Nifti1Image(X_rot, np.eye(4))
        return nii

    def rotate90(X):
        """
        Rotate a 3D image 90 degrees
        """
        return nib.Nifti1Image(np.rot90(X), np.eye(4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data augmentation with standard techniques')
    parser.add_argument("-i", "--input", type=str, required=True, help="path to input image")    #input CT image we can call by "-i" command
    parser.add_argument("-o", "--output", type=str, help="path to output image")                  #output tranformed image we can call by "-o" command
    parser.add_argument('-tech', type=str, help='technique')

    args = parser.parse_args()
    data = nib.load(os.path.join(args.input)).get_fdata()
    img_brightness = Data_aug.brightness(data)
    img_flipped = Data_aug.flip3D(data)
    img_rot30 = Data_aug.rotation_zoom3D(data)
    img_rot90 = Data_aug.rotate90(data)
    if args.tech == "brightness":
        nib.save(img_brightness, os.path.join(args.output, "brightness_img.nii.gz"))
    elif args.tech == 'flipping':
        nib.save(img_flipped, os.path.join(args.output, "flipped_img.nii.gz"))
    elif args.tech == "rotation30":
        nib.save(img_rot30, os.path.join(args.output, "rot30_img.nii.gz"))
    elif args.tech == "rotation90":
        nib.save(img_rot90, os.path.join(args.output, "rot90_img.nii.gz"))    
    else :
        raise TypeError("You have to choise a technique, like brightness, flipping, rotation30, rotation90")

