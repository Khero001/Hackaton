import pygame.midi
import time
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(65)
for i in range(24,96):
    player.note_on(i, 127)
    print(i)
    time.sleep(1)
    player.note_off(i, 127)
    
pygame.midi.quit()
