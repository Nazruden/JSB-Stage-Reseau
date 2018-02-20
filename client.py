#!/usr/bin/python3
####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : client.py
## Programme client du morpion aveugle
####################################

from cmdClient import *
from grid import *
from outils import *
import select
import socket
import sys


def prompt():
    sys.stdout.flush()

### Main client
def main():

    ## Définition des informations de connexion
    host = ""
    if len(sys.argv) < 2:
        print('Utilisation : python3 mainClient.py hostname\n')
        print('Hostname manquant.\n')
        host = input('Préciser hostname : ')
        sys.exit()
    else:
        host = sys.argv[1]
    port = 7777
    connexion = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    ## Connection au serveur
    connect_to_server(connexion, host, port)


    while True:
        ## Flux entrants - Terminal et hôte distant
        socket_list = [sys.stdin, connexion]
        # Récupération des différents sockets à l'instant T
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        # Parcours des sockets en attente de lecture
        for sock in read_sockets:
            # Lecture d'un message provenant de l'hôte distant
            if sock == connexion:
                data = sock.recv(1500)
                # Message vide : déconnexion du serveur
                if not data:
                    print('\nDisconnected from server')
                    sys.exit()
                else:
                    # Analyse paquets serveur
                    cmds = split_data(data)
                    
                    for cmd in cmds:
                        print(cmd)
                        # START
                        if cmd.startswith(b"START"):
                            # TODO : Gérer la réception du START

                        # STATE
                        if cmd.startswith(b"STATE"):
                            cmd_getstate(cmd_convert_data_to_grid(cmd))

                        # YOURTURN
                        if cmd.startswith(b"YOURTURN"):
                            # TODO : Gérer la réception d'un YOURTURN

                        # SCORE
                        if cmd.startswith(b"SCORE"):
                            # TODO : Gérer la réception du SCORE

                        # END
                        if cmd.startswith(b"END"):
                            # TODO : Gérer la réception d'un END
            # Lecture d'une entrée utilisateur
            else:
                msg = sys.stdin.readline()
                connexion.send(msg)
    pass

main()
