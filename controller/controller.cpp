#include <iostream>
#include "controller.h"

int getCurrentPath() {
    if (OS == "Linux" || OS == "macOS X" || OS == "OpenBSD" || OS == "QNX") { //El sistema operativo es una distro de GNU
      char szTmp[32];
      sprintf(szTmp, "/proc/%d/exe", getpid());
      int bytes = MIN(readlink(szTmp, pBuf, len), len - 1);
      if(bytes >= 0) {
        pBuf[bytes] = '\0';
      } else {
        return bytes;
      }
    } else if (OS == "Windows") { //El sistema operativo es Windows
      int bytes = GetModuleFileName(NULL, pBuf, len);
      if(bytes == 0) {
        return -1;
      } else {
        return bytes;
      }
    }
}

int main() {
  currentPath = getCurrentPath();
  system("python3 " + currentPath + "/" + MAINSCREEN_FILE); //ejecuta mainScreen.py
  return 0;
}
