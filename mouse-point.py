#!/usr/bin/env python
import numpy as np
import sys
import cv2

# local modules
import scan

dragging_flags = np.array([False, False, False, False])
points = [(100, 100), (100, 200), (200, 200), (200, 100)]

def get_distance(r1, r2):
    r1, r2 = map(np.array, [r1, r2])
    distance = np.sqrt(((r1 - r2)**2).sum())
    return distance

def onmouse(event, x, y, flags, param):
    global points, dragging_flags
    img = origin.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        # start dragging
        for idx, point in enumerate(points):
            if get_distance(point, (x,y)) < 7:
                points[idx] = (x, y)
                dragging_flags[idx] = True
    elif event == cv2.EVENT_LBUTTONUP:
        # end dragging
        if True in dragging_flags:
            idx = np.where(dragging_flags == True)[0][0]
            points[idx] = (x, y)
            dragging_flags[idx] = False
    elif True in dragging_flags:
        # while dragging, update points
        idx = np.where(dragging_flags == True)[0][0]
        points[idx] = (x, y)

    for point in points:
        cv2.circle(img=img, center=point, radius=5,
                color=(0,255,0), thickness=2)
    cv2.imshow("origin", img)

if __name__ == '__main__':
    cv2.namedWindow("origin", 1)
    cv2.setMouseCallback("origin", onmouse)

    # load original frame
    origin = cv2.imread('00.png', 1)

    # Show initial frame
    initial_frame = origin.copy()
    for point in points:
        cv2.circle(img=initial_frame, center=point, radius=5,
                color=(0,255,0), thickness=2)
    cv2.imshow("origin", initial_frame)

    while True:
        key = cv2.waitKey(2)
        if key == 27:
            sys.exit()
        elif key == ord('s'):
            four_points = np.array(points)
            scanned = scan.get_scanned(img=origin,
                    four_points=four_points,
                    output_shape=(200, 200))
            cv2.imshow('scanned', scanned)

    cv2.destroyAllWindows()
