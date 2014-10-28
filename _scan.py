#-*- coding: utf-8 -*-
# scan.py
import numpy as np

from skimage import transform as tf

def get_scanned(img, four_points, output_shape):
    w, h = output_shape
    out_points = np.array([(0, 0), (0, w), (h, w), (h, 0)])

    tform3 = tf.ProjectiveTransform()
    tform3.estimate(out_points, four_points)
    warped = tf.warp(img, tform3, output_shape=output_shape)
    return warped
