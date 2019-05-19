import pygame, sys, time, random
from pygame.locals import *


def mover(B,camera_pos):
    pos_x,pos_y = camera_pos # Split camara_pos
    #
    key = pygame.key.get_pressed() # Get Keyboard Input
    if key[pygame.K_w]:
        # Check Key
        B[1] -= 8 # Move Player Rect Coord
        pos_y += 8 # Move Camara Coord Against Player Rect
    if key[pygame.K_a]:
        
        B[0] -= 8
        pos_x += 8
    if key[pygame.K_s]:
        
        B[1] += 8
        pos_y -= 8
    if key[pygame.K_d]:
        
        B[0] += 8
        pos_x -= 8
    
    #
    if B[0] < 0: # Simple Sides Collision
        B[0] = 0 # Reset Player Rect Coord
        pos_x = camera_pos[0] #Reset Camera Pos Coord
    elif B[0] > 984:
        B[0] = 984
        pos_x = camera_pos[0]
    if B[1] < 0:
        B[1] = 0
        pos_y = camera_pos[1]
    elif B[1] > 984:
        B[1] = 984
        pos_y = camera_pos[1]
    #
    return (pos_x,pos_y) # Return New Camera Pos

pygame.init()
mundo=pygame.Surface((1000,1000))
V=pygame.display.set_mode((500,500))


Negro=(0,0,0)
Blanco=(255,255,255)
Rojo=(255,0,0)
Verde=(0,255,0)
Azulo=(0,0,255)
Azulc=(51,153,255)
Morado=(102,0,102)
Amarillo=(255,255,0)
Gris=(110,110,110)
Naranja=(252,152,3)

cambiox=0
cambioy=0

B=pygame.Rect(0,0,20,20)
reloj=pygame.time.Clock()
camara=((B[0]+15)+250,(B[1]+15)+250)
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
           pygame.quit()
           sys.exit()
    V.fill(Negro) # Esto es lo que te faltaba!!!
    mundo.fill(Azulc)
   
    pygame.draw.rect(mundo,Verde,(-300,-300,1000,1000))
    
    
    camara=mover(B,camara)
    pygame.draw.rect(mundo,Azulo,(300,300,50,50))

    pygame.draw.rect(mundo,Rojo,B)
    





    


    V.blit(mundo,camara)
    pygame.display.update()
    print(B[0],B[1])
    reloj.tick(60)
