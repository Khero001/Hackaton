from test import resize_img, read_line
import cv2

image = cv2.imread('pic2hcl/black_hole.jpg', 1)

resize_img(image, 200)

image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

row_count = 0
num_rows = image.shape[0]

hsl_matrix = []

for y in range(num_rows):
    row = read_line(image, row_count)
    hsl_matrix.append(row)

print (hsl_matrix)