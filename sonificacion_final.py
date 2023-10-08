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

def hls2note(hsl):
    note=0
    h,l,s = hsl[0],hsl[1],hsl[2]
    #todas en octava 4
    if(h>=172 or h<=7):
        note=60 # C
    elif(h>7 and h<=22):
        note=61 # C#
    elif(h>22 and h<=37):
        note=62 # D
    elif(h>37 and h<=52):
        note=63 # D#
    elif(h>52 and h<=67):
        note=64 # E
    elif(h>67 and h<=82):
        note=65 # F
    elif(h>82 and h<=97):
        note=66 # F#
    elif(h>97 and h<=112):
        note=67 # G
    elif(h>112 and h<=127):
        note=68 # G#
    elif(h>127 and h<=142):
        note=69 # L
    elif(h>142 and h<=157):
        note=70 # L#
    elif(h>157 and h<=172):
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
    
    return note,s

def hls2(hsl):
    note=0
    h,l,s = hsl[0],hsl[1],hsl[2]
    #todas en octava 4
    if(h>=172 or h<=7):
        note=60 # C
    elif(h>7 and h<=22):
        note=61 # C#
    elif(h>22 and h<=37):
        note=62 # D
    elif(h>37 and h<=52):
        note=63 # D#
    elif(h>52 and h<=67):
        note=64 # E
    elif(h>67 and h<=82):
        note=65 # F
    elif(h>82 and h<=97):
        note=66 # F#
    elif(h>97 and h<=112):
        note=67 # G
    elif(h>112 and h<=127):
        note=68 # G#
    elif(h>127 and h<=142):
        note=69 # L
    elif(h>142 and h<=157):
        note=70 # L#
    elif(h>157 and h<=172):
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


































