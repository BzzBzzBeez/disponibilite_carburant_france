#!/usr/bin/python3

#Script dispo Carburants France
#Made by BzzBzz - 18/10/2022

from xml.dom import minidom
from discord_webhook import DiscordWebhook
import os
import wget
import shutil


#Récupération url webhook discord

urlwebhook = open("id.txt","r")
url_api = str(urlwebhook.read().strip())
urlwebhook.close()
message = ""

#Input

f = open("info.txt", "r")
lines = f.readlines()
#print(lines)
f.close()

#Supprimer l'ancien fichier
if os.path.exists("PrixCarburants_instantane.zip"):
    os.remove("PrixCarburants_instantane.zip")
if os.path.exists("PrixCarburants_instantane.xml"):
    os.remove("PrixCarburants_instantane.xml")

# #Téléchargement du nouveau fichier
remote_url="https://donnees.roulez-eco.fr/opendata/instantane"
local_file="PrixCarburants_instantane.zip"
wget.download(remote_url,local_file)
print("\n")

#Dezipage fichier
shutil.unpack_archive("PrixCarburants_instantane.zip")

#Récupération Prix Carburants Bois d'Arcy
doc = minidom.parse("PrixCarburants_instantane.xml")
pdvs = doc.getElementsByTagName("pdv")

message = "```"
for line in lines:
    for pdv in pdvs:
        if pdv.getAttribute("cp") == line.strip():
            for i in pdv.getElementsByTagName("prix"):
                adresse = pdv.getElementsByTagName("adresse")[0].childNodes[0].data
                ville = pdv.getElementsByTagName("ville")[0].childNodes[0].data
                nom = str(i.attributes["nom"].value)
                prix = str(i.attributes["valeur"].value)
                message += (ville + " : " + adresse + " : " + nom + " : " + prix + "\n")
                print(ville + " : " + adresse + " : " + nom + " : " + prix)
    print("\t")
message += '```\n <@PUT_DISC_USER_ID>' #To be tagged
webhook = DiscordWebhook(url=url_api, content=message)
response = webhook.execute()
