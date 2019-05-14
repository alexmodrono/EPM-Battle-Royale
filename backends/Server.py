import socket, threading, sys, time, json, ast, os
from multiprocessing import Process, Pipe
from halo import Halo

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Server():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	names = []
	addresses = []
	coords = {}
	# {"Players": {"Player 1": {"x": 100, "y": 300, "w": 30, "h": 30}}}

	def __init__(self):
		self.sock.bind(('0.0.0.0', 10000))
		self.sock.listen(1)

		self.coords["Players"] = []
		self.dataToSend = ''
		self.dataDict = {}

	def handler(self, c, a):
		while True:
			data = c.recv(1024)
			##print(str(data, 'utf-8'))
			if str(data, 'utf-8')[0] == 'z' and str(data, 'utf-8')[1] == 'z':
				self.names.append(str(data, 'utf-8').replace('z', ''))
				name = self.names[self.addresses.index(a)]
			else:
				print(str(a[0]) + ' : ' + str(a[1]) + ' (' + str(name) + ') ' ' --> ' + str(data, 'utf-8'))

				#print(str(data, 'utf-8'))
				try:
					self.dataDict = ast.literal_eval(str(data, 'utf-8'))
				except:
					pass

				try:
					#print('Coords  ' + str(self.coords) + ' ---', self.dataDict)
					for item in self.coords["Players"]:
						if list(item.keys())[0] == name:
							self.coords["Players"][self.coords["Players"].index(item)][name] = self.dataDict[name]


					##for item in self.coords["Players"]:
					##	if list(item.keys())[0] == name:
					##		self.coords["Players"].append(self.dataDict)

				except:
					pass

				self.dataToSend = self.coords
			if not data:
				self.connections.remove(c)
				c.close()
				break

	def handler2(self, c, a):
		parsed = {}
		while True:
			for connection in self.connections:
				connection.send(bytes(str(self.dataToSend), 'utf-8'))

			time.sleep(1/60)

	def run(self):
		while True:
			c, a = self.sock.accept()
			self.addresses.append(a)

			cThread = threading.Thread(target=self.handler, args=(c, a))
			cThread.daemon = True
			cThread.start()
			cThread2 = threading.Thread(target=self.handler2, args=(c, a))
			cThread2.daemon = True
			cThread2.start()

			self.connections.append(c)
			self.coords["Players"].append({str(self.names[self.addresses.index(a)]): {"x": 100, "y": 300}})

			print(self.connections)
			print(self.names)

credits = """Autor: Miguel Garnica.
Colaboradores: Alejandro Modroño (@aedev) & Lukasits"""
os.system("clear")
print(color.PURPLE + "Ejecutando EPM Server v1.0..." + color.END)
for letter in credits:
  sys.stdout.write(letter)
  sys.stdout.flush()
  time.sleep(0.1)
print("\n")
try:
	loaderText = color.YELLOW + "Servidor ejecutándose..." + color.END
	loader = Halo(text=loaderText, spinner='dots')
	loader.start()
	server = Server()
	server.run()
except Exception as e:
	failText = "[" + color.PURPLE + "Error" + color.END + "] " + color.RED + "An error ocurred during runtime. ;("
	loader.fail(failText)
	print(e)
