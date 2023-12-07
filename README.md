# Data Precessing

## Data-augmentation-and-quality-evaluation
Data augmentation and quality evaluation of generated data

To use this, it is recommended to clone the codebase directly:

```Python 
git clone https://github.com/IsmailAbys/Data-augmentation-and-quality-evaluation.git
cd Data-augmentation-and-quality-evaluation
```

## Installation
we used the `Python==3.9.18`
Before executing the code, you must first install the libraries in the requirements file and make sure you have the correct versions installed.

`pip install -r requirements.txt`

Or create a conda environnement with `pre-process` by excuting
```Python
conda env create -f pre-process 
```

## Python scripts and their function
The folder `data_augmentation` contains all files, so you can use :.
```Python
cd data_augmentation
```

This script `data_aug.py` contains all functions (brightness, flipping, 30° and 90° rotation) and run it with \
```Python 
python data_aug.py -i "path of the input image" -o "path of the output folder" -tech "Transformation technique"
```
For the transformation technique, you choose "brightness" for the brightness technique, "flipping" to flip the image, "rotation30" to rotate the image 30°, and "rotation90°" for 90° rotation.


---
## Quantitative analysis
`MSE.py`, `ssim.py` and `Distance_euclidean.py` are the metrics for evaluating the quality of the images generated. Run
```Python 
python file.py -img1 "path of the first input image" -img2 "path of the second input image.
```

## Cropping
In our context, cropping involves centering the images to eliminate empty portions of the volume.
to run the script `crop.py`, you need to execute it :
```Python 
python crop.py -img1 "path of the first input image" -img2 "path of the output folder for the cropped imagee".
```

## Resampling 
The folder resampling contains, the script for resampling, to run it, you need to execute:
```Python
python resampling.py  --data-dir "path of the input data"  -x "size of x" -y "size of y" -z "size of z" --out-dir "output path" 
```

Inside the 'utils' folder, you can find some utility scripts, for example, to plot histograms, plot slices, or 3D visualization. To run, you can execute it in the following way:
```Python 
python file.py -i "path of input image"
```
For the example 
```Python 
python histograms.py -i "path of input image"
```
will give us, the histogram of input image, ![Screenshot](https://github.com/IsmailAbys/DataPrecessing/blob/main/utils/Figure_1.png)
