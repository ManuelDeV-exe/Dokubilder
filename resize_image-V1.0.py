"""
*************************************************
*            !!!INFO!!!                         *
*************************************************
* Programmname:     Rezise_Doku                 *
* Version:          1.0                         *
* Bescheibung:      Ändert die Größe der        *
*                   Dokubilder auf 1024x724     *
*                   und Dreht das Bild um 90°   *
*                                               *
* Letzte Änderung:  15.10.2020                  *
* Author:           Bücherl Manuel              *
* Status:           funktionsfähig              *
* Projekt:          Vereinfachung               *
* Python-Verion     python-3.9.0                *
*************************************************
"""

### Programm Start ###
from PIL import Image
import os
import shutil 
import os.path
from tkinter import messagebox 
import tkinter as tk

### Funktionen ###

def Pfad_Bereinigen(pfad):
    pfad = pfad.replace('\n', '')
    return pfad

config = open("config.cfg", "r") # Config lesen
configArray = config.readlines()

breite = int(configArray[7])
hoehe = int(configArray[10])

ServerPfad = Pfad_Bereinigen(configArray[1]) # Pfad auf Server auf den verschoben werden soll.
#Soll das Bild nicht verschoben werden, einfach nichts in die Gänsefüßchen schreiben.

BilderInDokuOrdner = os.listdir(Pfad_Bereinigen(configArray[4]))
aktuellerPfad = os.path.abspath(str(Pfad_Bereinigen(configArray[4]))) # Aktuellen Pfad der Datei festlegen
aktuellerPfad = aktuellerPfad.replace('\\', '/') # Pfad bereinigen
FileNotExist = True

config.close()

root = tk.Tk()
root.withdraw()

schleife = 0
while schleife < len(BilderInDokuOrdner):
    FileNotExist = True
    
    BidlerDatei = aktuellerPfad + "/" + BilderInDokuOrdner[schleife]
    
    filenameList = aktuellerPfad.split("\\")
    i = len(filenameList)-1 # Die anzahl der Pfadverzeichnisse -1 zur erzeugung des Uhrsprünglichen Bildnamens
    filename = filenameList[i]
    
    image1 = Image.open(BidlerDatei)

    if image1.size[0] < image1.size[1]:
        output = image1.resize((hoehe, breite))
        output = output.transpose(Image.ROTATE_270)
    else:
        output = image1.resize((breite, hoehe))
        
        
    if os.path.isfile(ServerPfad + '/' + BilderInDokuOrdner[schleife]):
        #str(ServerPfad + '/' + BilderInDokuOrdner[schleife])
        MsgBox = messagebox.askquestion("Datei Existiert bereits!", 'Die Datei: ' + str(ServerPfad + '\\' + BilderInDokuOrdner[schleife]) + ' Überschreiben?') 
        if MsgBox == 'yes':
            ServerPfad = ServerPfad.replace('\\', '/')
            print(str(ServerPfad + '/' + BilderInDokuOrdner[schleife]))
            os.remove(ServerPfad + '/' + BilderInDokuOrdner[schleife])
            os.remove(BidlerDatei) # Original löschen
            output.save(str(ServerPfad)+ '/' + str(BilderInDokuOrdner[schleife]), optimize=True, quality=100, dpi=(300,300))
        else:
            print('Datei ' + str(BilderInDokuOrdner[schleife]) + ' wurde behalten. Vorgang Abgebrochen.')
            os.remove(BidlerDatei) # Original löschen
        FileNotExist = False
    else:
        os.remove(BidlerDatei) # Original löschen
        output.save(str(aktuellerPfad) + "\\" + str(BilderInDokuOrdner[schleife]), optimize=True, quality=100, dpi=(300,300))
    
    if ServerPfad != "" and FileNotExist == True:
        ServerPfad = ServerPfad.replace('\\', '/') # Pfad bereinigen
        shutil.move(BidlerDatei, ServerPfad) 
    
    schleife = schleife + 1