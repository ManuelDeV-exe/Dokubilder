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

breite = int(configArray[10])
hoehe = int(configArray[13])

ServerPfad = Pfad_Bereinigen(configArray[1]) # Pfad auf Server auf den verschoben werden soll.
#Soll das Bild nicht verschoben werden, einfach nichts in die Gänsefüßchen schreiben.
if (Pfad_Bereinigen(configArray[4]) == "true"):
    ServerPfad = ServerPfad.split("\\", 1)
    ServerPfad[1] = ServerPfad[1].replace('\\', '/') # Pfad bereinigen
    ServerPfad = ServerPfad[0] + "/" + ServerPfad[1]

BilderInDokuOrdner = os.listdir(Pfad_Bereinigen(configArray[7]))
aktuellerPfad = os.path.abspath(str(Pfad_Bereinigen(configArray[7]))) # Aktuellen Pfad der Datei festlegen
aktuellerPfad = aktuellerPfad.split("\\", 1)
aktuellerPfad[1] = aktuellerPfad[1].replace('\\', '/') # Pfad bereinigen
FileNotExist = True

config.close()

root = tk.Tk()
root.withdraw()

for img in BilderInDokuOrdner:
    if len(img)>25:
        os.rename(aktuellerPfad[0] + "/" + aktuellerPfad[1] + "/" + img, aktuellerPfad[0] + "/" + aktuellerPfad[1] + "/" + img[:25] + ".jpg",)

BilderInDokuOrdner = os.listdir(Pfad_Bereinigen(configArray[7]))

schleife = 0
while schleife < len(BilderInDokuOrdner):
    FileNotExist = True
    
    BidlerDatei = aktuellerPfad[0] + "/" + aktuellerPfad[1] + "/" + BilderInDokuOrdner[schleife]
    
    image1 = Image.open(BidlerDatei)

    if image1.size[0] < image1.size[1]:
        output = image1.resize((hoehe, breite))
        output = output.transpose(Image.ROTATE_270)
    else:
        output = image1.resize((breite, hoehe))
        
        
    if os.path.isfile(str(ServerPfad) + '/' + BilderInDokuOrdner[schleife]):
        #str(ServerPfad + '/' + BilderInDokuOrdner[schleife])
        MsgBox = messagebox.askquestion("Datei Existiert bereits!", 'Die Datei: ' + str(ServerPfad + '\\' + BilderInDokuOrdner[schleife]) + ' Überschreiben?') 
        if MsgBox == 'yes':
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
        output.save(str(aktuellerPfad[0]+ "/" +aktuellerPfad[1]) + "/" + str(BilderInDokuOrdner[schleife]), optimize=True, quality=100, dpi=(300,300))
    
    if ServerPfad != "" and FileNotExist == True:
        shutil.move(BidlerDatei, ServerPfad) 
    
    schleife = schleife + 1