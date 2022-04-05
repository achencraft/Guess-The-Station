# Guess The Station

Ce code développé en Python Kivy est une application pour Androïd proposant un blind test des annonces sonores des trams de Strasbourg  


Remplasser le token et le lien URL dans service/update.py    
Attention, le fichier compressé avec les musiques n'est volontairement pas sur ce dépôt 


Installation

>apt install python3.8-venv libssl-dev  
>apt-get install android-tools-adb  
>python3 -m venv .  
>source bin/activate  
>pip3 install --upgrade buildozer plyer cython kivy oscpy kivymd requests pillow mapview playsound

Pour executer sur pc, il faut utiliser le python du virtuel env  
> python3 main.py  
> ou bin/python3 main.py

Pour compiller l'apk et l'installer sur le téléphone  
>buildozer android debug deploy run  

Pour juste compiler l'apk dans bin  
>buildozer android debug


>deactivate



------------------------------------

DEBUG android  
Pour avoir les logs de l'app dans un terminal  

Brancher le téléphone en USB et activer le déboggage par USB  
>apt-get install android-tools-adb  
>adb devices  

Pour le front  
>adb logcat --pid=$(adb shell pidof -s org.pm.pm)

Pour le back  
>adb logcat --pid=$(adb shell pidof -s org.pm.pm:service_Update)
