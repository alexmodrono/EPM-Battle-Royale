import pygame, sys, time, random, math
from pygame.locals import *


pygame.init()

V=pygame.display.set_mode((800,800),0,32)

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

reloj=pygame.time.Clock()

balas=[]
p=(800/2)-5
contador=5
abajo=False
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

        if event.type==MOUSEBUTTONDOWN:
            abajo=True

        if event.type==MOUSEBUTTONUP:
            abajo=False
            contador=2

    if abajo and contador>0:
        contador-=1





            
    while abajo and contador<=0:
        l=[]
        hip=math.sqrt(((event.pos[0]-p)**2)+((event.pos[1]-p)**2))
        v=100/hip
        l.append(p)
        l.append(p)
        l.append(((event.pos[0]-p)*v)/12)
        l.append(((event.pos[1]-p)*v)/12)
        balas.append(l)
        print(l)
        print(balas)
        contador=2


        

            
            


    V.fill(Negro)
    pygame.draw.rect(V,Rojo,(p,p,10,10))
    for i in range(len(balas)):
        balas[i][0]+=balas[i][2]
        balas[i][1]+=balas[i][3]
        pygame.draw.rect(V,Azulo,(balas[i][0],balas[i][1],5,5))

    for x in range(len(balas)-1):
        try:
            if balas[x][0]<=-5 or balas[x][0]>=800 or balas[x][1]<=-5 or balas[x][1]>=800:
                balas.remove(balas[x])

        except:
            pass



    pygame.display.update()

    reloj.tick(60)

        
