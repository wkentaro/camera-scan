import numpy as np

from skimage import measure
from skimage import color


def get_largest_contour(img):
    # gray scale
    gray = color.rgb2gray(img)

    # Find contours at a constant value of 0.8
    contours = measure.find_contours(gray, 0.8)

    def get_contour_maxpos(contour):
        ymax, ymin = contour[:, 0].max(), contour[:, 0].min()
        xmax, xmin = contour[:, 1].max(), contour[:, 1].min()
        return (xmax, xmin), (ymax, ymin)

    def calc_area(contour):
        (xmax, xmin), (ymax, ymin) = get_contour_maxpos(contour)
        area = (xmax - xmin) * (ymax - ymin)
        return area

    areas = np.array([calc_area(contour) for contour in contours])
    max_idx = np.where(areas.max())[0][0]

    (xmax, xmin), (ymax, ymin) = get_contour_maxpos(contours[max_idx])

    xmax, xmin, ymax, ymin = map(int, [xmax, xmin, ymax, ymin])

    return [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
