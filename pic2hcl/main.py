from test import resize_img, read_line_by_line
import cv2

image = cv2.imread('pic2hcl/black_hole.jpg', 1)

resize_img(image, 200)
hsl_matrix = read_line_by_line(image)

print (hsl_matrix)