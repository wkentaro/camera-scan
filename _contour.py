import numpy as np
import cv2


def get_largest_contour(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh,
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[1]
    approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)

    return approx
