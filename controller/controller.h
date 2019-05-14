//
//  main.h
//  Battle-Royale
//
//  Created by Alex Modroño Vara on 05/05/2019.
//  Copyright © 2019 Escuela Pensamiento Matemáctico. All rights reserved.
//
#include "stdc++.h"

#pragma once

#define AUTHORS "@aedev", "Miguel Garnica", "Lucasits", "Alejandro Modroño"
#define VERSION "1.0b2019f001"

#define MAINSCREEN_FILE "mainScreen.py"
#define HOST_BACKEND "Server.py"
#define CLIENT_BACKEND "Client.py"

#define STATE_GAME_PAUSED 0 //El juego está pausado, da igual el proceso que estuviese haciendo.
#define STATE_MAINSCREEN 1 //El usuario se encuentra en la pantalla principal.
#define STATE_SERVER_BACKEND 2 //El usuario está cargando el backend del servidor, es decir, es host. Este proceso está en segundo plano.
#define STATE_CLIENT_BACKEND 3 //El usuario no es host

#if defined(_WIN32)
  #define OS "Windows"
#elif defined(__linux__)
  #define OS "Linux"
#elif defined(__APPLE__)
  #define OS "macOS X"
#elif defined(BSD)
  #define OS "OpenBSD"
#elif defined(__QNX__)
  #define OS "QNX"
#endif
