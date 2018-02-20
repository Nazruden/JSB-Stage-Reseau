####################################
## JSB Stage - Le morpion aveugle ##
####################################
## Fichier : outils.py
## Outils pouvant être utilisés par le côté client et le côté serveur
####################################

def formalizedata(msg, cmd):
    return msg.replace(cmd, "").replace("\n", "")

def split_data(data):
    return data.split('\n')

def sendAll(clients, msg):
    for client in clients:
        client.send(msg)


def sendError(client, msg):
    client.send("ERROR " + msg)