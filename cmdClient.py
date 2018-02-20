####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : cmdClient.py
## Outils client
####################################
from grid import *
from outils import *
import select
import socket
import sys

# CMD Interface - Client version

def cmd_convert_data_to_grid(data):
    data = formalizedata(data ,"STATE ")
    tmp = data.split(" ")
    cells = []
    for elem in tmp:
        cells.append(int(elem))
    grid_instance = grid()
    grid_instance.cells = cells
    return grid_instance


# Connexion au serveur
def connect_to_server(socket, host, port):
    try:
        socket.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host.\nWelcome on MORPION\n')


# Gestion des retours de commandes
def cmd_getstate(grid):
    grid.display()

# Fonction d'affichage du score
def cmd_getscore(score):
    print("SCORE : " + score)

# Fonction pour demander au joueur de jouer une case
def cmd_play():
    place = -1
    while place > 8 or place < 0:
        place = input("Choisir une case entre 0 et 8\n")
    return "PLACE " + str(place)

    