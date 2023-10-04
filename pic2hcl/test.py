import cv2

image = cv2.imread('black_hole.jpg', 1)

#Image at most of 200x200 pixels
needs_resize = False
largest_side = image.shape.index(max(image.shape))
resize_factor = 200

if image.shape[largest_side] > resize_factor:
    resize_element = largest_side
    needs_resize = True

if needs_resize:
    scale_percent = 100 - ((image.shape[resize_element] - resize_factor)/image.shape[resize_element])*100
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

#Display stuff
'''if image is None:
    #sys.exit("Could not read the image")
    print("No image to display")
else:
    cv2.imshow("Display window", image)
    
    while True:
        k = cv2.waitKey(-1)
    
        if k == ord("c"):
            print("Image closed")
            break
    
    cv2.destroyAllWindows()'''  
        
hsl_matrix = []

"""
The shape attribute for numpy arrays returns the dimensions of the array. 
If Y has n rows and m columns, then Y.shape is (n,m). So Y.shape[0] is n.
"""
    
for y in range(image_hsl.shape[0]):
    row = []
    for x in range(image_hsl.shape[1]):
        pixel = image_hsl[y, x]
        hsl_value = ((pixel[0]/255)*180, (pixel[2]/2.55), (pixel[1]/2.55))
        row.append(hsl_value)
    hsl_matrix.append(row)

print(hsl_matrix)
