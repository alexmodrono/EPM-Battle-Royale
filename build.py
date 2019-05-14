import sys, os, time, random
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

def main():
    loaderText = color.PURPLE + "Compilando archivos..." + color.END
    loader = Halo(text=loaderText, spinner='dots')
    loader.start()
    os.system("g++ controller/controller.cpp -o EPM\ Battle\ Royale")
    loader.stop()

try:
    if sys.argv[1] == "dependencies":
        os.system("python3 -m pip install -r dependencies.txt")
        main()
    elif sys.argv[1] == "build":
        main()
    else:
        print(color.RED + "Por favor pasa algún argumento a " + color.END + color.BOLD + "npm start" + color.END + color.RED + "como " + color.BOLD + "-- dependencies" + color.END + o + color.BOLD + "-- build" + color.END + ".")
except Exception:
    print(color.RED + "Por favor pasa algún argumento a " + color.END + color.BOLD + "npm start" + color.END + color.RED + "como " + color.BOLD + "-- dependencies" + color.END + o + color.BOLD + "-- build" + color.END + ".")
