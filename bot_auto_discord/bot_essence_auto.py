#!/usr/bin/python3

#Script dispo Carburants France
#Made by BzzBzz - 18/10/2022

from xml.dom import minidom
from discord_webhook import DiscordWebhook
from datetime import datetime
import os
import sys
import wget
import shutil

CONST_OLD_NAME = "PrixCarbuOLD.xml"
CONST_NEW_NAME = "PrixCarburants_instantane.xml"


#Supprimer les anciens fichiers
if os.path.exists("PrixCarburants_instantane.zip"):
    os.remove("PrixCarburants_instantane.zip")
if os.path.exists("PrixCarburants_instantane.xml"):
    os.remove("PrixCarburants_instantane.xml")

#Téléchargement du nouveau fichier
remote_url="https://donnees.roulez-eco.fr/opendata/instantane"
local_file="PrixCarburants_instantane.zip"
wget.download(remote_url,local_file)
print("\n")

#Dezipage fichier
shutil.unpack_archive("PrixCarburants_instantane.zip")

#Check présence fichier old (Sinon renommer en old)
if not os.path.exists(CONST_NEW_NAME):
    print("Ancien fichier non présent, relance dans 10 minutes...")
    sys.exit()
else:
    os.rename(CONST_NEW_NAME,CONST_OLD_NAME)

#Récupération du Code Postal
if os.path.exists("info.txt"):
    f = open("info.txt", "r")
    lines = f.readlines()
    f.close()
else:
    print("Fichier 'info.txt' n'éxiste pas...")
    sys.exit()

#Récupération URL webhook discord
if os.path.exists("id.txt"):
    urlwebhook = open("id.txt","r")
    url_api = str(urlwebhook.read().strip())
    urlwebhook.close()
else:
    print("Fichier 'id.txt' n'éxiste pas...")

#Récupération Prix Carburants OLD
doc = minidom.parse(CONST_OLD_NAME)
pdvs = doc.getElementsByTagName("pdv")

OLD_tab=[]

for line in lines:
    for pdv in pdvs:
        if pdv.getAttribute("cp") == line.strip():
            for i in pdv.getElementsByTagName("prix"):
                ville = pdv.getElementsByTagName("ville")[0].childNodes[0].data
                OLD_tab.append(pdv.getElementsByTagName("ville")[0].childNodes[0].data + " : " + pdv.getElementsByTagName("adresse")[0].childNodes[0].data  + " : " + str(i.attributes["nom"].value))

#Récupération Prix Carburants NEW
doc = minidom.parse(CONST_NEW_NAME)
pdvs = doc.getElementsByTagName("pdv")

NEW_tab=[]

for line in lines:
    for pdv in pdvs:
        if pdv.getAttribute("cp") == line.strip():
            for i in pdv.getElementsByTagName("prix"):
                ville = pdv.getElementsByTagName("ville")[0].childNodes[0].data
                NEW_tab.append(pdv.getElementsByTagName("ville")[0].childNodes[0].data + " : " + pdv.getElementsByTagName("adresse")[0].childNodes[0].data  + " : " + str(i.attributes["nom"].value))

#Comparaison Prix Carburant OLD et NEW
liste_carb = ""
diff = set(NEW_tab).difference(OLD_tab)
for i in diff:
    liste_carb += (str(i) + "\n")

#Envoie sur le channel Discord si ajout d'un carburant
if not liste_carb == "":
    print(liste_carb)
    webhook = DiscordWebhook(url=url_api, content=liste_carb)
    response = webhook.execute()
else:
    print("Il n'y a pas eu d'ajout de carburant :'(")

#Affichage de la date dans le cas de log cronjob
now = datetime.now()
date_time = now.strftime("%H:%M:%S -- %m/%d/%Y")

print(date_time + "\n")

liste_carb = "```" + liste_carb #Mise en forme discord
liste_carb += "```<@259029103716466688>" #Put User ID to be tag
