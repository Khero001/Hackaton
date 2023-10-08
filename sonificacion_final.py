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

def hls2noteInst(hsl):
    note=0
    h,l,s = hsl[0],hsl[1],hsl[2]
    #todas en octava 4
    if(h>=244.375 or h<=10.625):
        note=60 # C
    elif(h>10.625 and h<=31.875):
        note=61 # C#
    elif(h>31.875 and h<=53.035):
        note=62 # D
    elif(h>53.035 and h<=74.285):
        note=63 # D#
    elif(h>74.285 and h<=95.535):
        note=64 # E
    elif(h>95.535 and h<=116.785):
        note=65 # F
    elif(h>116.785 and h<=138.035):
        note=66 # F#
    elif(h>138.035 and h<=159.285):
        note=67 # G
    elif(h>159.285 and h<=180.535):
        note=68 # G#
    elif(h>180.535 and h<=201.785):
        note=69 # L
    elif(h>201.785 and h<=223.035):
        note=70 # L#
    elif(h>223.035 and h<=243.285):
        note=71 # B
  
    if( l>=0 and l<42):
        note-=36
    elif( l>=42 and l<85):
        note-=24
    elif( l>=85 and l<127):
        note-=12
    elif( l>=127 and l<170):
        note=note
    elif( l>=170 and l<212):
        note+=12
    elif( l>=212 and l<=255):
        note+=24
    
    
    '''
    #usar l para nota 2 de acorde:
    #((l-tope inferior)/2)-21 = salto[va de -21 a 21]
    
    #s para nota 3 y *desfase y octava de la anterior
    
    [4,7]
    [3,7]
    '''
    return note,s*100



'''
def img2matrixNotesInstruments(image_hsl):
    notes=[]

    for y in range(image_hsl.shape[0]):
        row = []
        for x in range(image_hsl.shape[1]):

            hsl_value = ((pixel[0]/255)*180, (pixel[2]/2.55), (pixel[1]/2.55))
            row.append(hsl_value)
        notes.append(row)

'''








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


































