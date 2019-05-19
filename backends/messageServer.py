# Save as server.py
# Message Receiver
import os
from socket import *
import halo as h

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

def main(host):
    host = ""
    port = 13000
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("Waiting to receive messages...")
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        print("Received message: " + data)
        if data == "exit":
            break
    UDPSock.close()
    os._exit(0)

try:
    if len(sys.argv[1]) >= 1:
        main(sys.argv[1])
except:
    print(color.RED + "Enrer")
