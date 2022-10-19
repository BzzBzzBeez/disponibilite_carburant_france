#!/usr/bin/python3

#Script dispo Carburants France
#Made by BzzBzz - 18/10/2022

from xml.dom import minidom
from time import sleep
import os
import wget
import shutil


#Input User
inp = ""
while inp != "x":
    print("Entrer Code Postal (ou x = execute, p = print list, d = delete) : ")
    inp = str(input().strip())
    if inp == "p":
        f = open("info.txt", "r")
        lines = f.readlines()
        f.close()
        print("Liste Code Postaux :")
        for line in lines:
            print(line.strip())
    elif inp == "x":
        print("Execute...")
    elif inp == "d":
        count = 0
        f = open("info.txt", "r")
        lines = f.readlines()
        f.close()
        print("Entrer la ligne à supprimer (q = quit):")
        for line in lines:
            print("Ligne {}: {}".format(count, line.strip()))
            count += 1
        inp2 = input()
        if inp2 != "q":
            inp2 = int(inp2)
            del lines[inp2]
            f = open("info.txt", "w+")
            for line in lines:
                f.write(line)
            f.close()
            print("Ligne : {} supprimée".format(inp2))
    else:
        f = open("info.txt", "a")
        f.write(inp+"\n")
        f.close()

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

for line in lines:
    #print("Ville : {}".format(line.strip()))
    for pdv in pdvs:
        if pdv.getAttribute("cp") == line.strip():
            for i in pdv.getElementsByTagName("prix"):
                adresse = pdv.getElementsByTagName("adresse")[0].childNodes[0].data
                ville = pdv.getElementsByTagName("ville")[0].childNodes[0].data
                nom = str(i.attributes["nom"].value)
                prix = str(i.attributes["valeur"].value)
                print(ville + " : " + adresse + " : " + nom + " : " + prix)
    print("\t")
