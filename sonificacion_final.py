import cv2
from midiutil import MIDIFile
import pygame.mixer
import pygame.midi
from time import sleep
import numpy as np
from collections import Counter

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
    inst=0
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
  
    if( l>=0 and l<25.5):
        note=0 # filtro de obscuro
    elif( l>=25.5 and l<63.45):
        note-=36 #octava 2
    elif( l>=63.45 and l<102):
        note-=12 #octava 3
    elif( l>=140.25 and l<178.5):
        note=note #octava 4
    elif( l>=178.5 and l<216.75):
        note+=12 #octava 5
    elif( l>=216.75 and l<=255):
        note+=24 #octava 6
    
    if(s>=0 and s<30.6):
        inst= 32 # 32 bajo acustico
        factor_nota=0.5
        note, inicio= doubleIns(note,36)
    elif(s>=30.6 and s<55.93):
        inst= 74 # flauta dulce
        factor_nota=0.5
        note, inicio= doubleIns(note,60)
    elif(s>=55.93 and s<80.46):
        inst= 40 # violin
        factor_nota=0.5
        note, inicio= doubleIns(note,60)
    elif(s>=80.46 and s<105.39):
        inst= 69 # corno ingles
        factor_nota=0.5
        note, inicio= doubleIns(note,36)
    elif(s>=105.39 and s<130.33):
        inst= 56 # trompeta
        factor_nota=0.5
        note, inicio= doubleIns(note,48)
    elif(s>=130.33 and s<155.26):
        inst= 46 # arpa
        factor_nota=1
        inicio=0
    elif(s>=155.26 and s<180.19):
        inst= 71 # clarinete
        factor_nota=0.5
        note, inicio= doubleIns(note,60)
    elif(s>=180.19 and s<205.13):
        inst= 79 # ocarina
        factor_nota=0.5
        note, inicio= doubleIns(note,60)
    elif(s>=205.13 and s<230.06):
        inst=48  # cuerdas 1 
        factor_nota=0.5
        note, inicio= doubleIns(note,60)
    elif( s>=230.06 and s<=255):
        inst= 0 # piano
        factor_nota=1
        inicio=0
    
    return note,inst,factor_nota, inicio
def doubleIns(nota,start):
    nota=nota-24
    if (nota>=36):
        nota=nota-36
        inicio=0.5
    else:
        inicio=0
    nota=start+nota
    return nota,inicio

def unique_vals_in_row (image, row_count):
    row = []
    for x in range(image.shape[1]):
        pixel = image[row_count, x]
        hl_inst = hls2noteInst(pixel) #[note, instrument]
        hl_inst_str = str(hl_inst[0]) + "/" + str(hl_inst[1]) + "/" + \
                        str(hl_inst[2]) + "/" + str(hl_inst[3]) #note/instrument
        if hl_inst_str not in row:
            hl_inst_str = hl_inst_str.split("/")
            unique_vals = [int(val) for val in hl_inst_str]
            row.append(unique_vals)
    return row

def n_vals_from_mode (image, row_count, n_mode):
    row = []
    complete_row = []
    for x in range(image.shape[1]):
        pixel = image[row_count, x]
        hl_inst = hls2noteInst(pixel)
        hl_inst_str = str(hl_inst[0]) + "/" + str(hl_inst[1]) + "/" + \
                        str(hl_inst[2]) + "/" + str(hl_inst[3])
        complete_row.append(hl_inst_str)
        result = [item for items, c in Counter(complete_row).most_common()
                                            for item in [items] * c]
    complete_row = list(set(result))
    if (len(complete_row) - 1) < n_mode:
        selection_row = complete_row[0:]
    else:
        selection_row = complete_row[:n_mode]
    for selection in selection_row:
        selection = selection.split("/") #Separa valor '12/3/0.5/4' a ['12', '3', '0.5', '4']
        individual_val_list = []
        for i in selection:  
            individual_val = float(i)
            individual_val_list.append(individual_val)
            
        row.append(individual_val_list)
    return row

def play (row, duration, player, instrument_dict):
    #print(row)
    for i in row:
        if i[3] == 0.0:
            player.note_on(int(i[0]), 127, instrument_dict[int(i[1])])
    
    sleep(duration/2)
    
    for i in row:
        if i[3] == 0.5:
            player.note_on(int(i[0]), 127, instrument_dict[int(i[1])])
        if i[2] == 0.5 and i[3] == 0.0:
            player.note_off(int(i[0]), 127, instrument_dict[int(i[1])])
            
    sleep(duration/2)
    
    for i in row:
        if(i[2] == 0.5 and i[3] == 0.5) or (i[2] == 1.0):
            player.note_off(int(i[0]), 127, instrument_dict[int(i[1])])

def write_notes (row, duration, time, midi, instrument_dict):
    #print(row)
    for i in row:
        midi.addNote(track=instrument_dict[int(i[1])]-1, channel=0, pitch=int(i[0]), time=time+(duration*i[3]), duration=duration*i[2], volume=127)


def main(nombre_imagen='test/estrellas5novena.png',real_time=False,duration=0.4,moda=5,resize=420):
    #lee img
    image = cv2.imread(nombre_imagen)
    #reduce img
    image= resize_img(image,resize)
    #img a color hls
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    #num max de líneas
    num_rows = image.shape[0]
    #dicionario de instrumentos
    instrument_dict = {32:1, 74:2, 40:3, 69:4, 56:5, 46:6, 71:7, 79:8, 48:9, 0:10}
    #generate MIDI or real time
    if real_time:
        #init real time
        pygame.midi.init()
        player = pygame.midi.Output(0)
        for key, val in instrument_dict.items():
            player.set_instrument(key, val)
        #itera por línea
        for row_number in range(num_rows):
            #Detecta valores más repetidos (ejemplo/default: 3)
            row = n_vals_from_mode(image, row_number, moda)
            #Reproduce por línea (duración max por nota de 0.6 sec)
            play(row, duration, player, instrument_dict)
    else:
        #proceso generación midi
        instruments=['bajo acustico','flauta dulce','violin','corno ingles','trompeta','arpa','clarinete','ocarina','cuerdas 1','piano']
        time=0
        MyMIDI = MIDIFile(10) # 10 tracks
        #inicializa los tracks
        for i in range(10):
            MyMIDI.addTrackName(i, 0, instruments[i])
            MyMIDI.addTempo(i,0, 60)
        #itera por línea
        for row_number in range(num_rows):
            #Detecta valores más repetidos (ejemplo/default: 3)
            row = n_vals_from_mode(image, row_number, moda)
            write_notes (row, duration, time, MyMIDI, instrument_dict)
            time=time+duration
        with open((nombre_imagen.split(".")[0])+"_sonification.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
    '''
    while True:
        cv2.imshow('imagen de prueba',image)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    '''
main()


































