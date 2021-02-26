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
*            !!!INSTALATION!!!                  *
*************************************************

Installiere Python.
Importiere die Libraries Pillow(PIL), OS, tkinter und Shutil.
Ändere den Pfad zum Server falls gewünscht. 
Achtung, das r vor dem Pfad wird benötigt!
Lege einen Ordner mit dem Namen Dokubilder an.

Dieser Ordner muss sich im selben Verzeichnis wie diese Datei befinden.
Ich Empfehle die Dokumente oder einen Unterordner auf dem Desktop.
Der Ordner und die Datei müssen Lokal auf dem Rechner liegen.

In PDF Creator den Dokuordner als Standartpfad angeben.
Die Einstellungen der BilderQualität bleibt gleich.
Außerdem muss eine Aktion hinzugefügt werden.
Klicke bei dem Standartprofil auf Aktion hinzufügen und wähle Programm aus.
Jetzt wähle diese Datei als Programmdatei aus, und bestätige mit OK.
Beim Zielverzeichnis muss auserdem noch der Hacken bei 
"Öffne Datei nach Speicher" und bei "Zeige Sofortaktionen an, nachdem die Dokumente konvertiert wurden"
entfernt werden.

Nachdem du dies gemacht hast sollte alles Fkuntionieren.
Gehe wie gewohnt auf Drucken und probiere es aus.
In dem Ordner deiner Wahl sollte sich nun die Gedrehte und herunter gerechnete Doku befinden.

*************************************************
"""
### Programm Start ###
from PIL import Image
import os
import shutil 
import os.path
from tkinter import messagebox 
import tkinter as tk

breite = 1024
hoehe = 724

ServerPfad = r"C:\Users\Detag\Desktop\Programmieren\test" # Pfad auf Server auf den verschoben werden soll.
#Soll das Bild nicht verschoben werden, einfach nichts in die Gänsefüßchen schreiben.

BilderInDokuOrdner = os.listdir('./Dokubilder') # Inkrementaler Pfad in den die doku gespeichert wird.
aktuellerPfad = os.path.abspath("./") # Aktuellen Pfad der Datei festlegen
aktuellerPfad = aktuellerPfad.replace('\\', '/') # Pfad bereinigen
FileNotExist = True

root = tk.Tk()
root.withdraw()

schleife = 0
while schleife < len(BilderInDokuOrdner):
    FileNotExist = True
    
    BidlerDatei = aktuellerPfad + '/Dokubilder/' + BilderInDokuOrdner[schleife]
    
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
        output.save(str(aktuellerPfad)+ '/Dokubilder/' + str(BilderInDokuOrdner[schleife]), optimize=True, quality=100, dpi=(300,300))
    
    if ServerPfad != "" and FileNotExist == True:
        ServerPfad = ServerPfad.replace('\\', '/') # Pfad bereinigen
        shutil.move(BidlerDatei, ServerPfad) 
    
    schleife = schleife + 1