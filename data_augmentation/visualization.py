import os
import numpy as np
import vispy
from vispy import app, scene
from vispy.visuals.transforms import STTransform
import nibabel as nib
import scipy.ndimage
import argparse

# Inspired by:
# https://github.com/pranathivemuri/vispy-example-3d/blob/master/display_numpy_volume.py
# create colormaps that work well for translucent and additive volume rendering



class ArrayView3D(object):

    def view3DArray(data):
        ArrayView3D.gain = 0.8
        ArrayView3D.gamma = 0.8
        canvas = scene.SceneCanvas(
            keys='interactive', size=(800, 600), show=True)
        
        # Set up a viewbox to display the image with interactive pan/zoom
        view = canvas.central_widget.add_view()
        
        # Create the volume visuals, only one is visible
        volume1 = scene.visuals.Volume(
            data, parent=view.scene, threshold=0.225)        
        
        fov = 60.
        cam2 = scene.cameras.TurntableCamera(
            parent=view.scene, fov=fov,
            name='Turntable')
        view.camera = cam2

        # Create an XYZaxis visual
        axis = scene.visuals.XYZAxis(parent=view)
        s = STTransform(translate=(50, 50), scale=(50, 50, 50, 1))
        affine = s.as_matrix()
        axis.transform = affine

        # Implement axis connection with cam2
        @canvas.events.mouse_move.connect
        def on_mouse_move(event):
            if event.button == 1 and event.is_dragging:
                axis.transform.reset()

                axis.transform.rotate(cam2.roll, (0,1, 0))
                axis.transform.rotate(cam2.elevation, (0,0,1))
                axis.transform.rotate(cam2.azimuth, (1,0,0))

                axis.transform.scale((50, 50, 0.001))
                axis.transform.translate((50., 50.))
         


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Euclidian distance mesure between two images')
    parser.add_argument("-i",  type=str, required=True, help="path to input image1")    
    args = parser.parse_args()
    image = nib.load(args.i).get_fdata()
    ArrayView3D.view3DArray(image)
    app.run()