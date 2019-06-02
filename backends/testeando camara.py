import pygame, sys, time, random, math, ast, json, socket, threading, pyautogui
from pygame.locals import *



userList = []
passwordList = []

file = open('Logins.txt')
fileLines = file.readlines()
for x in fileLines:
	users = []
	pwds = []
	coma1Found = False
	for y in x:
		if y != ';' and y != '\n':
			if not coma1Found:
				users.append(y)
			elif coma1Found:
				pwds.append(y)

		if y == ';':
			coma1Found = True

	userList.append(''.join(users))
	passwordList.append(''.join(pwds))
print(userList)
print(passwordList)
user = 0

file.close()

uName = None

if pyautogui.confirm(text='Login or register:', title='Login', buttons=['Login', 'Register', 'Back']) == 'Login':
	while True:
		uName = pyautogui.prompt(text='Username', title='Login', default='')
		if uName in userList:
			for x in range(len(userList)):
				if userList[x] == uName:
					user = x
					while True:
						pwd = pyautogui.password(text='Password', title='Login', default='', mask='*')
						if pwd == passwordList[user]:
							pyautogui.alert(text='Done', title='Login', button='OK')
							break
						elif pwd == None:
							break

						else:
							pyautogui.alert(text='Incorrect password. Try again', title='Login error', button='OK')
		elif uName == None:
			break

		else:
			pyautogui.alert(text='Incorrect usrename. Try again', title='Login error', button='OK')
			continue
		break

if uName == None:
	Finish()

playerName = "Player " + uName
zzName = "zz" + playerName


def mover(B, camera_pos):
	pos_x, pos_y = camera_pos
	key = pygame.key.get_pressed()
	if key[pygame.K_w]:
		B[1] -= 8
		pos_y += 8
	if key[pygame.K_a]:
		B[0] -= 8
		pos_x += 8
	if key[pygame.K_s]:
		B[1] += 8
		pos_y -= 8
	if key[pygame.K_d]:
		B[0] += 8
		pos_x -= 8

	if B[0] < 0:
		B[0] = 0
		pos_x = camera_pos[0]
	elif B[0] > 1980:
		B[0] = 1980
		pos_x = camera_pos[0]
	if B[1] < 0:
		B[1] = 0
		pos_y = camera_pos[1]
	elif B[1] > 1980:
		B[1] = 1980
		pos_y = camera_pos[1]

	return (pos_x, pos_y)


pygame.init()
mundo = pygame.Surface((2000, 2000))
V = pygame.display.set_mode((1280, 720))

Negro = (0, 0, 0)
Blanco = (255, 255, 255)
Rojo = (255, 0, 0)
Verde = (0, 255, 0)
Azulo = (0, 0, 255)
Azulc = (51, 153, 255)
Morado = (102, 0, 102)
Amarillo = (255, 255, 0)
Gris = (110, 110, 110)
Naranja = (252, 152, 3)

cambiox = 0
cambioy = 0

B = pygame.Rect(0, 0, 20, 20)
reloj = pygame.time.Clock()
camara = ((B[0] + 15) + 640, (B[1] + 15) + 360)

contador = 5
abajo = False
balas = []
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == MOUSEBUTTONDOWN:
			abajo = True

		if event.type == MOUSEBUTTONUP:
			abajo = False
			contador = 2

	if abajo and contador > 0:
		contador -= 1
	V.fill(Negro)
	mundo.fill(Azulc)

	while abajo and contador <= 0:
		try:
			pos = pygame.mouse.get_pos()
			l = []
			largo = (pos[0] - 640)
			alto = (pos[1] - 360)
			hip = math.sqrt((largo ** 2) + (alto ** 2))
			v = 100 / hip
			l.append(B.centerx)
			l.append(B.centery)
			l.append((largo * v) / 12)
			l.append((alto * v) / 12)
			balas.append(l)
			contador = 2
		except:
			pass

	mundo.fill(Verde)

	camara = mover(B, camara)

	pygame.draw.rect(mundo, Rojo, B)

	pygame.draw.rect(mundo, Naranja, (150, 250, 50, 50))

	print({plar})





	for i in range(len(balas)):
		balas[i][0] += balas[i][2]
		balas[i][1] += balas[i][3]
		pygame.draw.rect(mundo, Azulo, (balas[i][0], balas[i][1], 5, 5))

	for x in range(len(balas) - 1, 0, -1):
		try:
			if balas[x][0] <= -5 or balas[x][0] >= 2000 or balas[x][1] <= -5 or balas[x][1] >= 2000:
				balas.remove(balas[x])

		except:
			pass
	V.blit(mundo, camara)
	pygame.display.update()
	reloj.tick(60)
