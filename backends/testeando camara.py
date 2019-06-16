import pygame, sys, time, random, math, ast, json, socket, threading, pyautogui
from pygame.locals import *

def WaitForKeyPress():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Finish()
			if event.type == pygame.KEYDOWN:
				return


def Finish():
	pygame.quit()
	sys.exit()


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

estoyLogin = False

while estoyLogin == False:

	uName = None

	mainMenu = pyautogui.confirm(text='Login or register:', title='Login', buttons=['Login', 'Register', 'Back'])

	if mainMenu == 'Login':
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
								estoyLogin = True
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

	elif mainMenu == 'Register':
		registerBox = pyautogui.confirm(text='Currently this function is not availiable.\nContact the developers if you do not have an account and you want to create one.', title='Register', buttons=['Back'])
		if registerBox == 'Back':
			pass

	elif mainMenu == 'Back':
		estoyLogin = True


if uName == None:
	Finish()

playerName = "Player " + uName
zzName = "zz" + playerName




velJugador = 5

def mover(B,camera_pos):
    pos_x,pos_y = camera_pos
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:

        B[1] -= velJugador
        pos_y += velJugador
    if key[pygame.K_a]:

        B[0] -= velJugador
        pos_x += velJugador
    if key[pygame.K_s]:

        B[1] += velJugador
        pos_y -= velJugador
    if key[pygame.K_d]:

        B[0] += velJugador
        pos_x -= velJugador


    if B[0] < 0:
        B[0] = 0
        pos_x = camera_pos[0]
    elif B[0] >anchoMapa-20:
        B[0] = anchoMapa-20
        pos_x = camera_pos[0]
    if B[1] < 0:
        B[1] = 0
        pos_y = camera_pos[1]
    elif B[1] > anchoMapa-20:
        B[1] = anchoMapa-20
        pos_y = camera_pos[1]


    parsed[playerName][0]["x"] = B[0]
    parsed[playerName][0]["y"] = B[1]


    return (pos_x,pos_y)

anchoPantalla = 800
largoPantalla = 600
anchoMapa = 2000
largoMapa = 2000
cadencia = 7

pygame.init()
mundo=pygame.Surface((anchoMapa,largoMapa))
V=pygame.display.set_mode((anchoPantalla,largoPantalla))
pygame.display.set_caption('EPM Battle Royale v1.0b2019f6')


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


maxBalaLifetime = 20
parsed = {playerName: [{"x": 100, "y": 100}, []]}

B=pygame.Rect(0,0,20,20)
reloj=pygame.time.Clock()
camara=((B[0]-10)+anchoPantalla//2,(B[1]-10)+largoPantalla//2)

contador=5
abajo=False
balas=[]





class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMsg(self):
		while True:
			if parsedCreated:
				self.sock.send(bytes(str(parsed), 'utf-8'))
			else:
				self.sock.send(bytes('Hola', 'utf-8'))
			time.sleep(1/60)

	def __init__(self, address):
		self.sock.connect((address, 10000))
		self.sock.send(bytes(zzName, 'utf-8'))
		time.sleep(1)

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()



WaitForKeyPress()

parsedCreated = False

client = Client(sys.argv[1])

while True:

	parsed = {playerName: [{"x": 100, "y": 100}, [], 100]}
	parsedCreated = True


	hecho = False

	while not hecho:

		V.fill(Negro)
		mundo.fill(Verde)


		data = client.sock.recv(1024)

		dataDict = {}
		dataProcessed = str(data, 'utf-8')

		if '}{' in str(data, 'utf-8'):
			dataProcessed = str(data, 'utf-8').split('}{')[0]
			dataProcessed = dataProcessed + '}'



		try:
			dataDict = ast.literal_eval(str(dataProcessed))
		except:
			pass

		if data:
			#print('Server --> ' + dataProcessed)
			print(dataDict)


		try:
			for playerItem in dataDict["Players"]:
				if list(playerItem.keys())[0] == playerName:
					parsed[playerName][2] = playerItem[playerName][2]
					for item in range(len(parsed[playerName][1])):
						parsed[playerName][1][item][2] = playerItem[playerName][1][item][2]

					if item[playerName][2] <= 0:
						print("MUERTO")
						Finish()

		except:
			pass

		try:
			for item in dataDict["Players"]:
				if list(item.keys())[0] != playerName:
					xPos = item[list(item.keys())[0]][0]["x"]
					yPos = item[list(item.keys())[0]][0]["y"]
					pygame.draw.rect(mundo, Azulo, (xPos, yPos, 20, 20))

					for bullet in item[list(item.keys())[0]][1]:
						if bullet[2] == 1:
							bulletX = bullet[0]
							bulletY = bullet[1]
							#bulletW = bullet[2]
							#bulletH = bullet[3]

							pygame.draw.rect(mundo, Blanco, (bulletX, bulletY, 5, 5))



		except:
			pass




		# ----------
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
			try:
				pos=pygame.mouse.get_pos()
				l=[]
				largo=(pos[0]-anchoPantalla//2)
				alto=(pos[1]-largoPantalla//2)
				hip=math.sqrt((largo**2)+(alto**2))
				v=100/hip
				l.append(B.centerx)
				l.append(B.centery)
				l.append((largo*v)/12)
				l.append((alto*v)/12)
				l.append(0) #Lifetime
				balas.append(l)
				parsed[playerName][1].append([B[0], B[1], 1])
				contador=cadencia
			except:
				pass




		camara=mover(B,camara)

		pygame.draw.rect(mundo,Rojo,B)


		for bala in balas:
			bala[4] += 1
			if bala[4] > maxBalaLifetime:
				balas.remove(bala)
				try:
					parsed[playerName][1].remove([int(bala[0]), int(bala[1]), 1])

				except:
					parsed[playerName][1].remove([int(bala[0]), int(bala[1]), 0])





		for i in range(len(balas)):
			balas[i][0]+=balas[i][2]
			balas[i][1]+=balas[i][3]
			pygame.draw.rect(mundo,Azulo,(balas[i][0],balas[i][1],5,5))
			parsed[playerName][1][i][0] = int(balas[i][0])
			parsed[playerName][1][i][1] = int(balas[i][1])

		'''for x in range(len(balas)-1,0,-1):
			try:
				if balas[x][0]<=-5 or balas[x][0]>=anchoMapa or balas[x][1]<=-5 or balas[x][1]>=largoMapa:
					balas.remove(balas[x])
	
			except:
				pass'''

		print(parsed)


		V.blit(mundo,camara)
		pygame.display.update()
		reloj.tick(60)
