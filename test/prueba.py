import cv2
import colorsys as cs
from midiutil import MIDIFile
import pygame.mixer
from time import sleep
import numpy as np
from io import StringIO
  
def reproduce_pixel(nota):
    # crea canal midi
    MyMIDI = MIDIFile(1) # 1 track
    MyMIDI.addTempo(0,0, 60)
    MyMIDI.addNote(0, 0, nota, 0, 0.5, 100)
    with open("test/notatemp.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)



    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load("test/notatemp.mid")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)
def rgb2hsl(color):
    h,l,s=cs.rgb_to_hls(color[0]/255,color[1]/255,color[2]/255)
    return round(h*360),s,l

def hsl2noteVol(hsl):
    note=0
    h,s,l = hsl[0],hsl[1],hsl[2]
    #todas en octava 4
    if(h>345 and h<=15):
        note=60 # C
    elif(h>15 and h<=45):
        note=61 # C#
    elif(h>45 and h<=75):
        note=62 # D
    elif(h>75 and h<=105):
        note=63 # D#
    elif(h>105 and h<=135):
        note=64 # E
    elif(h>135 and h<=165):
        note=65 # F
    elif(h>165 and h<=195):
        note=66 # F#
    elif(h>195 and h<=225):
        note=67 # G
    elif(h>225 and h<=255):
        note=68 # G#
    elif(h>255 and h<=285):
        note=69 # L
    elif(h>285 and h<=315):
        note=70 # L#
    elif(h>315 and h<=345):
        note=71 # B
    
    #print(note)
    if( l>=0 and l<0.1667):
        note-=36
    elif( l>=0.1667 and l<0.3334):
        note-=24
    elif( l>=0.3334 and l<0.5):
        note-=12
    elif( l>=0.5 and l<0.6668):
        note=note
    elif( l>=0.6668 and l<0.8335):
        note+=12
    elif( l>=0.8335 and l<=1):
        note+=24

    return note,s*100
def hls2noteVol(hsl):
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
    
    return note,s*100
def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
        print(f'coordenadas ({y},{x})')
        reproduce_pixel(hls2noteVol( hsv_img[y][x] )[0])
        print("h: "+str((hsv_img[y][x][0]/255)*180)+"°    s: "+str(hsv_img[y][x][2]/2.55)+"%    l: "+str(hsv_img[y][x][1]/2.55)+"%")
        print("nota: "+str(hls2noteVol( hsv_img[y][x] )[0]))
      # put coordinates as text on the image
      #cv2.putText(img, f'({x},{y})',(x,y),
      #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
      # draw point on the image
      #cv2.circle(img, (x,y), 3, (0,255,255), -1)



# lee imagen
img = cv2.imread('C:/Users/Optimen/Documents/Hackaton/test/pb.jpg')
cv2.namedWindow('test2')
cv2.setMouseCallback('test2', click_event)

# crea canal midi
MyMIDI = MIDIFile(1) # 1 track
MyMIDI.addTempo(0,0, 60)


a=300
b=180
#image[row][col]
aux=0
'''
array_notas=[]
for i, row in enumerate(img):
    for j, pixel in enumerate(img[0]):
        aux+=1
        print(img[i][j])
        pitch,vol=hsl2noteVol( rgb2hsl(img[i][j]) )
        array_notas.append(pitch)

def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

'''
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
#print(" son: "+str(aux))

#print( img[a][b] )
#print(hsv_img[a][b])
#print( rgb2hsl(img[a][b]) )
#print( hsl2noteVol( rgb2hsl(img[a][b]) ) )

#MyMIDI.addNote(track, channel, pitch, time, duration, volume)
#degrees  = [60, 62, 64, 65, 67, 69, 71] # MIDI note number
#octava N notas [x,y] rango en L
#octava 1  [60, 71]
#octava 2  [36, 47]
#octava 3  [48, 59]
##octava 4  [60, 71]
#octava 5  [72, 84]
#octava 6  [85, 96] 
degrees =[ hsl2noteVol( rgb2hsl(img[a][b]) )[0] ]
#degrees = [60,64,67]
time     = 0   # cuando inicia
duration = 0.5   # duracion
volume=100
#volume   = round(hsl2noteVol( rgb2hsl(img[a][b]) )[1]) # 0-127, as per the MIDI standard

for nota in degrees:
    
    MyMIDI.addNote(0, 0, nota, time, duration, volume)
    time = time +0.5








while True:
   cv2.imshow('test2',img)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows()






with open("test/sound.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("test/sound.mid")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)
print ("Done!")