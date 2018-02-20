####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : game.py
## Classe Game : gestion du jeu
####################################

import socket
from grid import *
from cmdServ import *
from outils import *


# Game class
class game:
    # Grids
    grids = [grid(), grid(), grid()]

    # Players and spectators
    players = dict()
    spectators = []
    currentPlayer = None
    gameReady = False

    # Scores
    scores = dict()

    # Game management
    # init Game
    def __init__(self):
        self.grid = grid()
        self.players = dict()
        self.scores = dict()
        self.currentPlayer = J1
        for i in [J1, J2]:
            self.players[i] = None
            self.scores[i] = 0

    ##########################################################
    ## Fonctions d'ajouts de joueurs / gestion des spectateurs
    ##########################################################
    # addPlayer method : Ajoute un joueur à la partie
    def addPlayer(self, client):
        # Essai d'affectation en joueur 1
        if self.players[J1] is None:
            self.players[J1] = client
            # TODO : envoi de l'état de la grille au joueur 1
        # Essai d'affectation en joueur 2
        elif self.players[J2] is None:
            self.players[J2] = client
            # TODO : envoi de l'état de la grille au joueur 
        # Sinon affectation aux spectateurs
        else:
            self.spectators.append(client)
            # TODO : une fois le cas typique géré
        # Plus de place disponibles pour les joueurs, début de la partie
        if not self.gameReady and self.players[J1] is not None and self.players[J2] is not None:
            self.gameReady = True
            self.startGame()

    # removeClient : retire un client (joueur ou spectateur) de la partie
    def removeClient(self, client):
        # Checking in players
        for player in [J1, J2]:
            if self.players[player] == client:
                self.players[player] = None
                # If game was running
                if self.gameReady:
                    self.gameReady = False
                    print("PAUSE - A PLAYER HAS LEFT")
                    self.sendAll("PAUSE - A PLAYER HAS LEFT\n")
        # Checking in spectators
        for spectator in self.spectators:
            if spectator == client:
                self.spectators.remove(client)

    # playerToSpectator method : déplace un joueur en spectateur
    def playerToSpectator(self, player):
        self.spectators.append(self.players[player])
        self.players[player] = None

    def spectatorToPlayer(self, spectator):
        self.spectators.remove(spectator)
        self.addPlayer(spectator)
    
    # joinGame method : gestion du join d'un spectateur
    def joinGame(self, client):
        self.spectatorToPlayer(client)

    #############################################    
    ## Action de joueur, début et fin de partie
    #############################################   
    # place method : place un jeton sur une case
    def place(self, player, cell):
        if cell is not "":
            cell = int(cell)
        if cell < 9 and cell >= 0:
            # Vérification : s'agit il du bon joueur
            if self.players[self.currentPlayer] == player:
                # Vérification : case vide
                if self.grids[0].isEmpty(cell):
                    # Mise à jour de la grille du joueur
                    self.grids[self.currentPlayer].cells[cell] = self.currentPlayer
                    # Mise à jour de la grille publique
                    self.grids[0].play(self.currentPlayer, cell)
                    # Envoi du nouvel état de la grille au joueur
                    # TODO : envoyer l'état de la grille au joueur courant

                    # Vérification de fin de partie
                    if self.grids[0].gameOver() > 0:
                        self.endGame()
                    # Sinon tour suivant
                    else:
                        self.currentPlayer = self.currentPlayer % 2 + 1
                # Case non vide
                else:
                    # Mise à jour de la grille du joueur
                    self.grids[self.currentPlayer].cells[cell] = self.grids[0].cells[cell]
                    # Envoi du nouvel état de la grille au joueur
                    # TODO : gestion du cas : le joueur a joué sur une case déjà jouée
                # Gestion de déroulement de partie : tour suivant
                if self.gameReady:
                    # TODO : informer le joueur courant qu'il doit jouer
            # Mauvais joueur
            else:
                sendError(player, "Ce n'est pas votre tour.\n")
        # Case invalide
        else:
            # TODO : gestion du cas d'erreur : case invalide

    # startGame method :
    def startGame(self):
        # Print game beginning and sends START and TURN tokens
        print("---- GAME STARTING ----")

        ####################################################
        # TODO : Signifier aux clients le début de la partie
        ####################################################

    # endGame method :
    def endGame(self):
        print("---- GAME ENDING ----")
        # Vérification d'un vainqueur - 0 sinon
        winner = self.grids[0].gameOver()
        
        ###############################################
        # TODO : Signifier aux clients la fin de partie
        ###############################################
        

    # isPlayer method : vérifie si le joueur passé en paramètre est le joueur courant
    def isPlayer(self, client):
        # Player 1
        if self.players[J1] == client:
            return J1
        # Player 2
        elif self.players[J2] == client:
            return J2
        # Spectator
        else:
            return 0

    # sendAll method : envoie un message à tous les clients (joueurs et spectateurs)
    def sendAll(self, msg):
        self.sendPlayers(msg)
        self.sendSpectators(msg)

    # sendPlayers method : envoie un message aux joueurs
    def sendPlayers(self, msg):
        for player in [J1, J2]:
            if self.players[player] is not None:
                self.players[player].send(msg)

    # sendSpectators method : envoie un message aux spectateurs
    def sendSpectators(self, msg):
        for spectator in self.spectators:
            spectator.send(msg)

    # sendScores method : envoi des scores à tout le monde
    def sendScores(self):
        self.sendAll(self.getScore())

    # sendState method : sends appropriate state to specified client
    def sendState(self, client):
        client.send(self.getState(client))

    # sendTurn method : envoi de l'information "VOTRE TOUR" au joueur précisé
    def sendTurn(self, player):
        player.send("YOURTURN\n")

    # getScore method : retourne les scores sous la forme d'une chaîne de caractères
    def getScore(self):
        prefix = "SCORE "
        return prefix + str(self.scores[J1]) + " " + str(self.scores[J2]) + "\n"

    # getState method : retourne l'état de la grille sous la forme d'une chaîne de caractères - 9 entiers concaténés séparés par un espace
    def getState(self, client):
        prefix = "STATE "
        # State J1 grid
        if self.isPlayer(client) == J1:
            return prefix + self.grids[J1].toString() + "\n"
        # State J2 grid
        elif self.isPlayer(client) == J2:
            return prefix + self.grids[J2].toString() + "\n"
        # State public grid
        else:
            return prefix + self.grids[0].toString() + "\n"
