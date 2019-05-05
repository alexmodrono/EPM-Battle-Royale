import pygame as pg
from pygame.locals import *
import sys
import time
import random
import os

pg.init()

#####################################################################
"<-- Clases y Objetos -->"

class Effect():
    def __init__(self, surface):
        self.object = surface

    def pulse(self, initialColor, finalColor, fadeTime): #changes to the initColor and then at the speed selected in fadeTime, changes it to the final color.
        self.initColor = initialColor
        self.finalColor = finalColor

        #newRGBToBeAdded = fadeTime//=60 #obtains the rgb that needs to be added each frame the effect lasts

    def direct(self, color): #directly changes the color to the color selected
        self.object.fill(color)

    def alpha(self, visibility, fadeTime): #changes object visibility at the fadeTime selected.
        pass

class Room():
    def __init__(self, paredes):
        self.listaParedes = pg.sprite.Group()

        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4])
            self.listaParedes.add(pared)

class Bloque(pg.sprite.Sprite):
    """
    Crea la clase bloque que hereda de la clase Sprite() ya programada
    en Pygame
    """

    def __init__(self, color, largo, alto, image=None, size=None, colorkey=None):
        super().__init__()

        #Define los atributos
        self.color = color
        self.largo = largo
        self.alto = alto

        #Crea la imagen y obtiene los datos
        self.image = pg.Surface([largo, alto])
        if colorkey is not None:
            self.image.fill(BLANCO)
            self.image.set_colorkey(colorkey)

        if image is not None:
            #Definir Sprites con imágenes
            self.image = pg.image.load(image).convert()

            if size is not None:
                self.image = pg.transform.scale(self.image, size)

            if colorkey is not None:
                self.image.set_colorkey(colorkey)
        else:
            #Dibuja el objeto
            pg.draw.rect(self.image, color, [0, 0, largo, alto])

        #crea la variable rect
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1

        if self.rect.y >= 720:
            self.rect.y = 30

class Pared(pg.sprite.Sprite):
    """
    Crea la clase pared que hereda de la clase Sprite() ya programada
    en Pygame
    """

    def __init__(self, color, largo, alto, x, y, image=None, size=None):
        super().__init__()

        #Define los atributos
        self.color = color
        self.largo = largo
        self.alto = alto

        #Crea la imagen y obtiene los datos
        self.image = pg.Surface([largo, alto])
        self.image.fill(color)
        self.image.set_colorkey(BLANCO)

        if image is not None:
            #Definir Sprites con imágenes
            self.image = pg.image.load(image).convert()

            if size is not None:
                self.image = pg.transform.scale(self.image, size)

            self.image.set_colorkey(BLANCO)
        #else:
            #Dibuja el objeto
            #pg.draw.rect(self.image, color, [x, y, largo, alto])

        #crea la variable rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pg.sprite.Sprite):
    """
    Crea la clase pared que hereda de la clase Sprite() ya programada
    en Pygame
    """

    def __init__(self, color, largo, alto, x, y, image=None, size=None, colorkey=None):
        super().__init__()

        #Define los atributos
        self.color = color
        self.largo = largo
        self.alto = alto

        self.habitacionActual = 0

        #Crea la imagen y obtiene los datos
        self.image = pg.Surface([largo, alto])
        self.image.fill(color)
        self.image.set_colorkey(NEGRO)

        if image is not None:
            #Definir Sprites con imágenes
            self.image = pg.image.load(image).convert()

            if size is not None:
                self.image = pg.transform.scale(self.image, size)

            if colorkey is not None:
                self.image.set_colorkey(colorkey)
        #else:
            #Dibuja el objeto
            #pg.draw.rect(self.image, color, [x, y, largo, alto])

        #crea la variable rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #atributos especiales
        self.cambioX = 0
        self.cambioY = 0
        self.paredes = None

    def update(self):
        self.rect.x+= self.cambioX
        listaImpactosParedes = pg.sprite.spritecollide(self, self.paredes, False)
        #comprueba si choca
        for pared in listaImpactosParedes:
            if self.cambioX > 0:
                self.rect.right = pared.rect.left
            elif self.cambioX < 0:
                self.rect.left = pared.rect.right

        self.rect.y+= self.cambioY
        listaImpactosParedes = pg.sprite.spritecollide(self, self.paredes, False)
        #comprueba si choca
        for pared in listaImpactosParedes:
            if self.cambioY > 0:
                self.rect.bottom = pared.rect.top
            elif self.cambioY < 0:
                self.rect.top = pared.rect.bottom

#####################################################################
"<-- Funciones -->"

def chocar(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        if (puntoDentroDeRect(a.left, a.top, b)) or (puntoDentroDeRect(a.left, a.bottom, b)) or (puntoDentroDeRect(a.right, a.top, b)) or (puntoDentroDeRect(a.right, a.bottom, b)):
            return True
    return False

def animarTexto(rectObject, finalPos):
    while True:
        rectObject[1].centerx-=10
        sv.blit(rectObject[0], rectObject[1])
        pg.display.update()
        print(rectObject[1].centerx)

        if rectObject[1].centerx == int(finalPos):
            print("Ya")
            break

def puntoDentroDeRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def getFont(size, fuente=None):
    tamaño = size

    if fuente is not None:
        fuente = pg.font.Font(fuente, tamaño)
    else:
        fuente = pg.font.Font("fuentes/FiraCode-Regular.ttf", tamaño)

    return fuente

def comprobarClick(pos, obj, nombre):
    if pos[0] >= obj.left and pos[0] <= obj.right and pos[1] >= obj.top and pos[1] <= obj.bottom:
                    return True
    else:
        return False

def getSize(obj):
    global x_centered
    global y_centered
    global w
    global h

    w, h = obj.size

    x_centered = 1280 / 2 - w / 2
    y_centered = 720 / 2 - h / 2


def escribir(texto, fuente, color, superficie, x, y, return1, left=False):
    objetoTexto = fuente.render(texto,1,color)
    rectanguloTexto = objetoTexto.get_rect()
    if left:
        rectanguloTexto.topleft = (x, y)
    else:
        rectanguloTexto.centerx = x
        rectanguloTexto.centery = y
    superficie.blit(objetoTexto, rectanguloTexto)
    if return1:
        return objetoTexto, rectanguloTexto

def terminar():
    pg.quit()
    sys.exit()

def comprobarClick(pos, obj, nombre):
    if pos[0] >= obj.left and pos[0] <= obj.right and pos[1] >= obj.top and pos[1] <= obj.bottom:
                    return True
    else:
        return False

def esperar():
    global instrucciones
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminar()
            if event.type == KEYUP:
                if event.key == K_f:
                    instrucciones= True
                return

#####################################################################
"<-- Colores -->"

# Colores
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
GRIS = (128, 128, 128)
LIMA = (0, 255, 0)
PURPURA = (128, 0, 128)
AMARILLO = (255, 255, 0)
MARRON = (118, 60, 40)
NOCHE = (6, 57, 113)
CL2 = (0, 40, 82)
DIA  = (0, 193, 255)
NARANJA = (235, 106, 14)
A2 = (236, 130, 86)
CL = (0, 135, 255)
ROJO_CLARO = (244, 92, 66)
FICHA_VERDE = (65, 244, 140)
FICHA_ROJA = (249, 89, 64)
JUGADOR_AZUL = (65, 187, 244)

DISCORD = (157, 165, 249)

#####################################################################
"<-- Variables -->"

ancho, alto = 1280, 720
sv = pg.display.set_mode((ancho, alto))
pg.display.set_caption("Juego Final Battle Royale v1.0")
#pg.mixer.music.load("musica/(3DS Music) Find Mii II - Save the World Heroes!.mp3")
#completado = pg.mixer.Sound("musica/stage_clear.wav")

# grupos de Sprites
listaParedes = pg.sprite.Group()
listaDeTodosLosSprites = pg.sprite.Group()

#x_centered = 1920 / 2 - image_width / 2
#y_centered = 1080 / 2 - image_height / 2

hecho = True

#####################################################################
"<-- Código del Juego (Bucles) -->"

while True:
    sv.fill(BLANCO)

    pg.display.update()
    for event in pg.event.get(): #eventos
        if event.type == QUIT:
            quit()
