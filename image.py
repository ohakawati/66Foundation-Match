import cv2
import numpy as np

src_img = cv2.imread('IMG_23.jpg')
average_color_row = np.average(src_img, axis=0)
average_color = np.average(average_color_row, axis=0)
print(average_color)

for color in average_color:
  print(color)