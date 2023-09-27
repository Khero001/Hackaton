import cv2
import colorsys as cs
from midiutil import MIDIFile
import pygame.mixer
from time import sleep
  
# lee imagen
img = cv2.imread('C:/Users/Optimen/Documents/Hackaton/test/pb.jpg')

# crea canal midi
MyMIDI = MIDIFile(1) # 1 track
MyMIDI.addTempo(0,0, 60)

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

a=100
b=120
#image[row][col]

for i, row in enumerate(img):
    for j, pixel in enumerate(img):
        aux=1
        #pitch,vol=hsl2noteVol( rgb2hsl(img[i][j]) )
            

print( img[a][b] )
print( rgb2hsl(img[a][b]) )
print( hsl2noteVol( rgb2hsl(img[a][b]) ) )




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
time     = 0   # cuando inicia
duration = 1   # duracion
volume   = round(hsl2noteVol( rgb2hsl(img[a][b]) )[1]) # 0-127, as per the MIDI standard

for nota in degrees:
    MyMIDI.addNote(0, 0, nota, time, duration, volume)
    time = time +0.5



with open("test/sound.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("test/sound.mid")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)
print ("Done!")