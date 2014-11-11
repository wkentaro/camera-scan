#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py

# standard libs
import sys
import argparse
# installed libs
import numpy as np
import cv2
# local libs
import _warp
import _contour
import pyutils


dragging_flags = np.array([False, False, False, False])
points = np.array([[100, 100], [100, 200],
                   [200, 200], [200, 100]])


def get_distance(r1, r2):
    r1, r2 = map(np.array, [r1, r2])
    distance = np.sqrt(((r1 - r2)**2).sum())
    return distance


def onmouse(event, x, y, flags, param):
    global points, dragging_flags
    width = 600
    scale = 1. * origin_size[0] / width
    dsize = (width, int(origin_size[1]/scale))
    img = cv2.resize(src=origin, dsize=dsize,
            interpolation=cv2.INTER_AREA)

    if event == cv2.EVENT_LBUTTONDOWN:
        # start dragging
        for idx, point in enumerate(points):
            if get_distance(point, (x,y)) < 10:
                points[idx] = [x, y]
                dragging_flags[idx] = True
    elif event == cv2.EVENT_LBUTTONUP:
        # end dragging
        if True in dragging_flags:
            idx = np.where(dragging_flags == True)[0][0]
            points[idx] = [x, y]
            dragging_flags[idx] = False
    elif True in dragging_flags:
        # while dragging, update points
        idx = np.where(dragging_flags == True)[0][0]
        points[idx] = [x, y]

    for point in points:
        cv2.circle(img=img, center=tuple(point), radius=5,
                color=(0,255,0), thickness=-1, lineType=cv2.CV_AA)
    cv2.polylines(img=img, pts=np.array([points]),
            isClosed=1, color=(0, 200, 0), lineType=cv2.CV_AA)
    cv2.imshow(winname='before', mat=img)


if __name__ == '__main__':
    # get img path
    img_path = sys.argv[1]

    # setup GUI params
    cv2.namedWindow(winname='before')
    cv2.setMouseCallback(window_name='before', on_mouse=onmouse)

    # load original frame
    origin = cv2.imread(filename=img_path, flags=1)
    origin_size = (origin.shape[1], origin.shape[0])

    # handle initial frame
    width = 600
    scale = 1. * origin_size[0] / width
    dsize = (width, int(origin_size[1]/scale))
    initial_frame = cv2.resize(src=origin, dsize=dsize,
            interpolation=cv2.INTER_AREA)
    # get contour
    points = _contour.get_largest_contour(img=initial_frame)
    if len(points) != 4:
        points = np.array([[100, 100], [100, 200],
                           [200, 200], [200, 100]])
    for point in points:
        cv2.circle(img=initial_frame, center=tuple(point), radius=5,
                color=(0, 255, 0), thickness=-1, lineType=cv2.CV_AA)
    cv2.polylines(img=initial_frame, pts=np.array([points]),
            isClosed=1, color=(0, 255, 0), lineType=cv2.CV_AA)

    cv2.imshow(winname='before', mat=initial_frame)

    # wait for user input
    while True:
        key = cv2.waitKey(2)
        # appoint the destinational size
        dsize = (None, None)
        if key == 27:
            sys.exit()
        elif key == ord('s'):
            dsize = (600, 600)
        elif key == ord('a'):
            dsize = (420, 600)
        # if dsize is appointed the img will be warped
        if None not in dsize:
            warped = _warp.get_warped(img=origin,
                    four_points=(scale * points),
                    output_shape=(dsize[1]*3, dsize[0]*3))
            resized = cv2.resize(src=warped, dsize=dsize,
                    interpolation=cv2.INTER_AREA)
            cv2.imshow(winname='after', mat=resized)
            filename = pyutils.get_filename_frompath(img_path)
            filename = pyutils.change_filename(filename=filename,
                    extension='_warped.png')
            cv2.imwrite('dst/'+filename, warped*255)

    cv2.destroyAllWindows()
