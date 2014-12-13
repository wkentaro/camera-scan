import numpy as np
import cv2


def get_largest_contour(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh,
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('get_contours', img)

    print contours
    if len(contours[1]) == 4:
        cnt = contours[1]
    else:
        cnt = contours[0]
    approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
    return np.reshape(approx, (len(approx), 2))
