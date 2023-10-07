import cv2
from midiutil import MIDIFile
import pygame.mixer
import pygame.midi
from time import sleep
import numpy as np

def resize_img(image, resize_factor):
    needs_resize = False
    largest_side = image.shape.index(max(image.shape))

    if image.shape[largest_side] > resize_factor:
        resize_element = largest_side
        needs_resize = True

    if needs_resize:
        scale_percent = 100 - ((image.shape[resize_element] - resize_factor)/image.shape[resize_element])*100
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image

def img2matrixNotesInstruments(image_hsl):
    notes=[]
    insts=[]

    for y in range(image_hsl.shape[0]):
        row = []
        for x in range(image_hsl.shape[1]):

            hsl_value = ((pixel[0]/255)*180, (pixel[2]/2.55), (pixel[1]/2.55))
            row.append(hsl_value)
        hsl_matrix.append(row)










def main():
    #lee img
    image = cv2.imread('test/pb.jpg')
    #reduce img
    image= resize_img(image,420)
    #img a color hls
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)


    while True:
        cv2.imshow('imagen de prueba',image)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()




main()


































