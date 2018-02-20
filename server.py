#!/usr/bin/python3
####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : server.py
## Programme serveur du morpion aveugle
####################################

from cmdServer import *
from game import *
from outils import *
import random
import select
import socket
import sys


# Main serveur
def main():
    ## Vars
    # Communication
    clients = list()
    spectators = list()
    # Game
    gameInstance = game()

    # Création d'un socket d'écoute - notre "oreille"
    ear = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ear.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ear.bind(('', 7777))
    ear.listen(3)
    print("Serveur lance")
    print("Attente de connexion...")
    
    ## Boucle principale
    while True:
        tmp = list(clients)
        tmp.append(ear)
        changes = select.select(tmp, list(), list())[0]
        ## Parcours des sockets en attente de lecture
        for client in changes:
            # Traitement du socket d'écoute
            if client == ear:
                data = client.accept()
                print("Nouvelle connexion de " + str(data[1]))
                # Ajout du client
                clients.append(data[0])
                # Ajout du client à la partie
                gameInstance.addPlayer(data[0])

            # Traitement
            else:

                data = client.recv(1500)

                # Traitement deconnexion
                if len(data) == 0:  # Si la longueur recue est 0 c'est que l'user s'est deconnecte
                    cmd_disconnect(gameInstance, clients, client)
                # CMD : DISCONNECT
                elif data.startswith(b"DISCONNECT"):
                    cmd_disconnect(gameInstance, clients, client)
                # TODO : gestion de PLACE et JOIN


    pass

main()
