import cv2
import numpy as np
def average_color(f, r, l):
    forehead = cv2.imread(f)
    right = cv2.imread(r)
    left = cv2.imread(l)

    forehead_average_color_row = np.average(forehead, axis = 0)
    forehead_average_color = np.average(forehead_average_color_row, axis = 0)

    right_average_color_row = np.average(right, axis = 0)
    right_average_color = np.average(right_average_color_row, axis = 0)

    left_average_color_row = np.average(left, axis = 0)
    left_average_color = np.average(left_average_color_row, axis = 0)

    average_color = (forehead_average_color + right_average_color + left_average_color) / 3

    return average_color