#!/usr/bin/env python
import numpy as np
import sys
import cv2

# local modules
import _warp
import _contour

dragging_flags = np.array([False, False, False, False])
points = np.array([[100, 100], [100, 200], [200, 200], [200, 100]])

def get_distance(r1, r2):
    r1, r2 = map(np.array, [r1, r2])
    distance = np.sqrt(((r1 - r2)**2).sum())
    return distance

def onmouse(event, x, y, flags, param):
    global points, dragging_flags
    width = 600
    scale = 1. * origin_size[0] / width
    dsize = (width, int(origin_size[1]/scale))
    img = cv2.resize(src=origin, dsize=dsize, interpolation=cv2.INTER_AREA)

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
    cv2.namedWindow(winname='before')
    cv2.setMouseCallback(window_name='before', on_mouse=onmouse)

    # load original frame
    origin = cv2.imread(filename=sys.argv[1], flags=1)
    origin_size = (origin.shape[1], origin.shape[0])

    # Show initial frame
    width = 600
    scale = 1. * origin_size[0] / width
    dsize = (width, int(origin_size[1]/scale))
    initial_frame = cv2.resize(src=origin, dsize=dsize, interpolation=cv2.INTER_AREA)

    points = _contour.get_largest_contour(img=initial_frame)
    if len(points) != 4:
        points = np.array([[100, 100], [100, 200], [200, 200], [200, 100]])
    for point in points:
        cv2.circle(img=initial_frame, center=tuple(point), radius=5,
                color=(0, 255, 0), thickness=-1, lineType=cv2.CV_AA)
    cv2.polylines(img=initial_frame, pts=np.array([points]),
            isClosed=1, color=(0, 255, 0), lineType=cv2.CV_AA)

    cv2.imshow(winname='before', mat=initial_frame)

    while True:
        key = cv2.waitKey(2)
        if key == 27:
            sys.exit()
        elif key == ord('s'):
            a4size = (420, 600)
            warped = _warp.get_warped(img=origin,
                    four_points=(scale * points),
                    output_shape=(a4size[1]*3, a4size[0]*3))
            cv2.imshow(winname='after',
                     mat=cv2.resize(src=warped, dsize=a4size, interpolation=cv2.INTER_AREA))
            cv2.imwrite('warped.png', warped*255)

    cv2.destroyAllWindows()
