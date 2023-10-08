import cv2
from midiutil import MIDIFile
import pygame.mixer
import pygame.midi
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
    pygame.mixer.music.load("test/notatemp.mid")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)
def hls2chord(hsl):
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
def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
        print(f'coordenadas ({y},{x})')
        reproduce_pixel(hls2chord( imgh[y][x] )[0])
        print("h: "+str((imgh[y][x][0]/255)*180)+"°    s: "+str(imgh[y][x][2]/2.55)+"%    l: "+str(imgh[y][x][1]/2.55)+"%")
        print("h: "+str(imgh[y][x][0])+"    s: "+str(imgh[y][x][2])+"    l: "+str(imgh[y][x][1])+"")
        
        print("nota: "+str(hls2chord( imgh[y][x] )[0]))

# inicia pygame para reproducir notas
pygame.init()
pygame.mixer.init()
# lee imagen
img = cv2.imread('C:/Users/Optimen/Documents/Hackaton/test/pb.jpg')
# cambia a hls *importante el orden, no es hsl
imgh = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
#1.411764705882353
# genera ventana y listener con el click
#cv2.namedWindow('test2')
#cv2.setMouseCallback('test2', click_event)
# crea canal midi
MyMIDI = MIDIFile(2) # 1 track
MyMIDI.addTempo(0,0, 60)
MyMIDI.addTempo(1,0, 60)





a=300
b=180
#image[row][col]


'''
array_notas=[[1]*imgh.shape[1] for x in range(imgh.shape[0])]
#array_segunda = [][]
#array_tercera = [][]

for i, row in enumerate(imgh):
    for j, pixel in enumerate(imgh[0]):
        #print(str(i)+" , "+str(j))
        

        array_notas[i][j]=hls2chord( imgh[i][j] )[0]
        
        #array_notas.append(pitch)

'''

#print( img[a][b] )
#print(imgh[a][b])
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

# arreglo de notas
degrees =[ 60,61,62,63,64,65,66,67,68,69,70,71,72 ]
#degrees = [60,64,67]
time     = 0   # cuando inicia
duration = 0.5   # duracion
volume=100
#volume   = round(hsl2noteVol( rgb2hsl(img[a][b]) )[1]) # 0-127, as per the MIDI standard

for nota in degrees:

    MyMIDI.addNote(0, 0, nota, time, duration, volume)
    time = time +0.5







'''
while True:
   cv2.imshow('test2',img)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows()
'''





with open("test/sound.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)


pygame.mixer.music.load("test/sound.mid")
pygame.midi.Output.set_instrument(40)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)
print ("Done!")
