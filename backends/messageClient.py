# Message Sender
import os
from socket import *
host = "192.168.1.36" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = input("Enter message to send or type 'exit': ")
    UDPSock.sendto(bytes(data, 'utf-8'), addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
