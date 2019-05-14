#include <iostream>
#include "controller.h"
#include <stdio.h>  /* defines FILENAME_MAX */
#include <Python.h>
/*
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
} */

std::string GetCurrentWorkingDir( void ) {
  char buff[FILENAME_MAX];
  GetCurrentDir( buff, FILENAME_MAX );
  std::string current_working_dir(buff);
  return current_working_dir;
}

int main() {
  std::cout << "EPM Battle Royale Controller v1.0 running in " << OS << std::endl;
  std::string currentDir = GetCurrentWorkingDir();
  if (OS == "Linux" || OS == "macOS X" || OS == "OpenBSD" || OS == "QNX") { //El sistema operativo es una distro de GNU
    std::string runMainScreenFileCommand = "python3 " + currentDir + MAINSCREEN_FILE;
  else if (OS == "Windows") {
    std::string runMainScreenFileCommand = "py " + currentDir + MAINSCREEN_FILE;
  }
  system(runMainScreenFileCommand.c_str()); //ejecuta mainScreen.py
  return 0;
}
