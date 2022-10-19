# Disponibilité Carburants - France
Envoie de messages en Webhook Discord automatiquement s'il y a eu un approvisionnement dans la(les) ville(s) sellectionée(s)<br>
Script à mettre dans un cronjob pour éxecution tout les X temps<br>
Exemple (5 mins):
```*/5 * * * * cd /home/user/folder && /usr/bin/python3.9 /home/user/folder/bot_carb_auto.py >> /home/user/folder/logbot.log```

# Important
Ajouter un fichier info.txt dans le repertoire du script avec les codes postaux des villes qui vous intéressent, exemple :<br>
![image](https://user-images.githubusercontent.com/55196216/196695139-ba3666c1-84b5-43b0-b3ef-493e9c728956.png)
<br>Ainsi qu'un fichier id.txt avec l'url de votre webhook discord !

Have Fun ;) !
