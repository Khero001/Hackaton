import pygame.midi
import time
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(8)
for i in (list(range(60,72))+list(range(84,96))):
    player.note_on(i, 127)
    print(i)
    time.sleep(0.3)
    player.note_off(i, 127)
    
pygame.midi.quit()
