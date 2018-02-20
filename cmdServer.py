####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : cmdServer.py
## Outils serveur
####################################

from game import *

# Fonction utilisée pour déconnecter un client proprement
def cmd_disconnect(game, clients, client):
    # Retrait du client de la liste des clients et de la partie puis fermeture du socket
    clients.remove(client)
    game.removeClient(client)
    client.close()    
    print("Client deconnecte")

# Envoi de l'état de la partie gameInstance du point de vue de client
def cmd_sendstate(client, gameInstance):
    client.send(gameInstance.getState(client))

# Envoi des scores au client
def cmd_sendscore(client, gameInstance):
    client.send(gameInstance.getScore())

# E
def cmd_place(client, gameInstance, data):
    client.send(gameInstance.place(client, data))


def cmd_start(players):
    for player in players:
        player.send("START\n")

# CMD Yourturn : inform a player he has to play
def cmd_yourturn(player):
    player.send("YOURTURN")

# CMD End : send END to players with endstate, an int for :
#               - 1 : player 1 victory
#               - 2 : player 2 victory
def cmd_end(players, endstate):
    for player in players:
        player.send("END " + endstate)
