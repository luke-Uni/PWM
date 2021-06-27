import subprocess
import secrets
import random
import time
import getpass
import threading
import base64
from cryptography.fernet import Fernet
import string
from colorama import Fore
from datetime import datetime, timedelta
import hashlib
import os

global crypter

#Es wird das übergebene Masterpasswort geprüft, indem die Zahlenfolge 12345 versucht wird mit dem aktuellen crypter zu entschlüsseln
def passwort_pruefung(pw):

    crypter_erstellen(pw)

    f = open('master_info.txt','rb')
    lines = f.readlines()
    k = entschluesseln(lines[0])
    f.close()

    if "12345" == k:
        return True
    else:
        return False

# aus dem übergebenen Masterpasswort wird ein crypter erstellt
def crypter_erstellen(pw):
    pw_hash = hashlib.sha256(pw.encode())

    pw_hexi = pw_hash.hexdigest()[:32]

    global crypter
    crypter = Fernet(base64.b64encode(pw_hexi.encode()))

# es wird dem übergebenen String tabs angehängt, abhängig der länge des Strings
def abstand(wort):

    if len(wort) < 8:
        return wort + "\t" + "\t" + "\t" + "\t"
    elif len(wort) < 16:
        return wort + "\t" + "\t" + "\t"
    elif len(wort) < 24:
        return wort + "\t" + "\t"
    elif len(wort) < 32:
        return wort + "\t"

# mit dem globalen crypter wird der übergebene String entschlüsselt
def entschluesseln(wort):
    global crypter
    try:
        entschluesselte_Nachricht = crypter.decrypt(wort).decode()

        return entschluesselte_Nachricht
    except:
        print("Masterpasswort ist falsch")

# mit dem globalen crypter wird der übergebene String verschlüsselt
def verschluesseln(wort):
    verschluesselte_Nachricht = crypter.encrypt(wort.encode())

    return verschluesselte_Nachricht

class Nutzerdaten ():
    
    #die attribute des Objektes werden deklariert
    def __init__(self):
        self.title = None
        self.code = None
        self.username = None
    #es wird geprüft ob Leerzeichen bei einem Titel Username oder Passwort eingegeben wurde
    def pruefe_einagbe(self):

        alles = self.title + self.username + self.code
        alles_liste = alles.split(" ")

        if len(alles_liste) > 1:
            print("Titel, Username, und Passwort dürfen keine Leerzeichen enthalten.")
            return False

        return True
    #daten werden auf einer Datei hinzugefügt
    def daten_hinzufuegen(self):
        
        erstellungsdatum = datetime.now()
        if self.pruefe_einagbe():
        #mit modus ab die daten in Bytes, der Datei hinzufügen
            f = open('nutzer_info.txt', 'ab')
            f.write(verschluesseln(self.title + " " + self.username + " " + self.code + " " + str(erstellungsdatum)))
            f.close
            f = open('nutzer_info.txt', 'a')
            f.write("\n")
            f.close()
        
    #gibt die ganze Datei farbig mit den Nutzerdaten als Tabelle aus
    def ganze_Liste_ausgeben(self):
        
        f = open("nutzer_info.txt", "rb")
        
        lines = f.readlines()
        f.close()
        f = open("nutzer_info.txt", "rb")
        print(Fore.LIGHTYELLOW_EX + abstand("Titel") + Fore.RESET + Fore.LIGHTGREEN_EX + abstand("Username")+ Fore.RESET + Fore.LIGHTRED_EX  + abstand("Passwort") + Fore.RESET + Fore.LIGHTMAGENTA_EX + "Erstellungsdatum" + Fore.RESET)
        print(Fore.LIGHTWHITE_EX + "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――" + Fore.RESET)
        for bit_line in lines:
            line = entschluesseln(bit_line)
            userdaten = line.split()
            print(Fore.LIGHTYELLOW_EX + abstand(userdaten[0])+ Fore.RESET + Fore.LIGHTGREEN_EX + abstand(userdaten[1]) + Fore.RESET + Fore.LIGHTRED_EX + abstand(verdecken(userdaten[2])) + Fore.RESET + Fore.LIGHTMAGENTA_EX + userdaten[3] + Fore.RESET)
            print(Fore.LIGHTWHITE_EX + "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――" + Fore.RESET)

        f.close()


class Thread1 (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    #Passwort soll nach 30 sekunden aus der Zwischenablage gelöscht werden
    def run (self):
        time.sleep(30)
        zwischenablage_löschen()
# ein übergbenes Passwort in die Zwischenablage speichern
def zwischenablage_speichern(txt):
    ablage ="echo "+txt.strip()+"|clip"
    subprocess.check_call(ablage, shell=True)

    #ein Thread erstellen um das Passwort unabhängig vom Hauptprozess aus der Zwischenablgae löschen
    t1 = Thread1()
    t1.start()

#die Zwischenablage zu Passwort gelöscht ändern
def zwischenablage_löschen():

    ablage="echo "+" Passwort gelöscht "+"|clip"
    subprocess.check_call(ablage, shell=True)

#gibt an ob Passwörter länger als 30 Tage alt sind
def pruefe_abgelaufene_passwoerter():
    f = open('nutzer_info.txt', 'rb')
    lines = f.readlines()
    abgelaufen = False

    for bit_line in lines:
        line = entschluesseln(bit_line)
        line = line.split()
        if datetime.strptime(line[3], "%Y-%m-%d") + timedelta(days = + 30) < datetime.now():
            print("Ändern Sie Ihr Passwort von " + line[0] + " " + line[1])
            abgelaufen = True
       
    if abgelaufen == False:
        print("Alle Passwörter sind noch nicht Abgelaufen.")

# erstellt ein Passwort mit der verlangten länge und sonstigen Anforderungen und speicher dies in der Zwischenablage
def password_generator():

    pw = ""
    kombiniert = ""

    zahlen = string.digits
    kleinbuchstaben = string.ascii_lowercase
    grossbuchstaben = string.ascii_uppercase
    sonderzeichen = "?,;._*!§%-#'-*()`´"
    
    soll_zahlen_enthalten = False
    soll_kleinbuchstaben_enthalten = False
    soll_grossbuchstaben_enthalten = False
    soll_sonderzeichen_enthalten = False

    anzahl_anforderungen = 0

    print("\nINFO: Sie können entscheiden, ob ihr Passwort Zahlen, Kleinbuchstaben, Großbuchstaben oder Sonderzeichen enthalten muss und welche Länge es entsprechen soll\n")   

    laenge = int(input("Bitte gib die Passwortlaenge ein: "))

    pruefe_zahlen = input("Sollen Zahlen im Passwort enthalten sein? \nJa=1/Nein=2: ")
    pruefe_kleinbuchstaben = input("Sollen Kleinbuchstaben im Passwort enthalten sein? \nJa=1/Nein=2: ")
    pruefe_grossbuchstaben = input("Sollen Großbuchstaben im Passwort enthalten sein? \nJa=1/Nein=2: ")
    pruefe_sonderzeichen = input("Sollen Sonderzeichen im Passwort enthalten sein? \nJa=1/Nein=2: ")

    if pruefe_zahlen == '1':
        anzahl_anforderungen += 1
        soll_zahlen_enthalten = True

    if pruefe_kleinbuchstaben == '1' and laenge > len(kombiniert):
        anzahl_anforderungen += 1
        soll_kleinbuchstaben_enthalten = True

    if pruefe_grossbuchstaben == '1' and laenge > len(kombiniert):
        anzahl_anforderungen += 1
        soll_grossbuchstaben_enthalten = True

    if pruefe_sonderzeichen == '1' and laenge > len(kombiniert):
        anzahl_anforderungen += 1
        soll_sonderzeichen_enthalten = True

    if laenge >= anzahl_anforderungen and anzahl_anforderungen >= 1:
        #Abfragen ob User bestimmte Zeichenkategorien haben möchte
        while laenge > len(kombiniert):
        
            if soll_zahlen_enthalten:
                kombiniert += secrets.choice(zahlen)

            if soll_kleinbuchstaben_enthalten and laenge > len(kombiniert):
                kombiniert += secrets.choice(kleinbuchstaben)

            if soll_grossbuchstaben_enthalten and laenge > len(kombiniert):
                kombiniert += secrets.choice(grossbuchstaben)

            if soll_sonderzeichen_enthalten and laenge > len(kombiniert):
                kombiniert += secrets.choice(sonderzeichen)
        
        #Passwort wird nochmal durchgemischt!
        pw = ''.join(random.sample(kombiniert,len(kombiniert)))

        print("Passwort: " + verdecken(pw) + " in Zwischenablge gespeichert.")

        zwischenablage_speichern(pw)
        time.sleep(0.2)
        passwortsicherheit(pw)

    elif laenge == 0:
        print("Passortlänge muss mindestens 1 betragen.")
    else:
        print("Sie können kein Passwort generieren mit " + str(anzahl_anforderungen) + " verschiednen Zeichenkategorien, wenn die Länge " + str(laenge) + " beträgt")

# gibt "*" in der Länge des übergbenen passworts zurück
def verdecken(pw):
    anzahl = len(pw)
    geheim_pw = ""

    while(anzahl > len(geheim_pw)):
        geheim_pw += "*"

    return str(geheim_pw)

# prüft ob der übergebene Titel in der Userdatendatei existiert
def exist(titel):
    f = open("nutzer_info.txt", "rb")
    lines = f.readlines()
    f.close()
    f = open("nutzer_info.txt", "r")
    for bit_line in lines:
        line = entschluesseln(bit_line)
        userdaten = line.split(" ")
        if titel.lower() == str(userdaten[0]).lower():
            f.close()
            return True
    return False

#gibt den eingegbenen titel mit titel, username und Passwort zurück
def nutzerdatei_finden():
    titel = input("Welchen Titel wollen Sie ansehen: ")
    f = open("nutzer_info.txt", "rb")
    if(exist(titel)):
        lines = f.readlines()
        f.close()
        f = open("nutzer_info.txt", "r")
        for bit_line in lines:
            line = entschluesseln(bit_line)
            userdaten = line.split(" ")
            if titel == userdaten[0]:
                print(Fore.LIGHTYELLOW_EX + userdaten[0] + Fore.RESET +  " " + Fore.LIGHTGREEN_EX + userdaten[1] + Fore.RESET + " " + Fore.LIGHTRED_EX + verdecken(userdaten[2]) + Fore.RESET)
                zwischenablage_speichern(userdaten[2])
    else:
        print("Titel ist nicht vorhanden.")                    

# der eingegebene titel soll aus der Nutzerdatendatei gelöscht werden
def nutzerdatei_loeschen():

    titel_delete = input("Welchen Titel wollen Sie löschen?\nTitel: ")

    if (exist(titel_delete)):
        bestaetigung = input("Sind sie Sicher das Sie die Nutzerdaten von " + titel_delete + " löschen wollen?\nGeben Sie 'Bestaetigen' ein um das Passwort unwiderruflich zu löschen! ")
        if bestaetigung == "Bestaetigen":
            f = open("nutzer_info.txt", "rb")
            lines = f.readlines()
            f.close()
            open('nutzer_info.txt', 'w').close()
            
            for bit_line in lines:
                line = entschluesseln(bit_line)
                userdaten = line.split(" ")
                
                if titel_delete not in userdaten[0]:
                    f = open('nutzer_info.txt', 'ab')
                    f.write(verschluesseln(line))
                    f.close()
                    f = open('nutzer_info.txt', 'a')
                    f.write("\n")
                    f.close()
            print(titel_delete + " wurde gelöscht")    
        else:
            print("Löschung wurde nicht bestätigt!")
    else:
        print("Titel ist nicht vorhanden.")
  
# Ändert den Username oder das Passwort, des eingegeben Titels
def nutzerdatei_aendern():
    titel = input("Geben Sie den Titel ein: ")
    if exist(titel):
        username = input("Geben Sie den Username ein: ")
        code  = str(getpass.getpass("Geben Sie das neue Passwort ein: "))
    
        f = open("nutzer_info.txt", "rb")
        lines = f.readlines()
        f.close()
        open('nutzer_info.txt', 'w').close()
            
        for bit_line in lines:
            line = entschluesseln(bit_line)
            userdaten = line.split(" ")
                
            if titel not in userdaten[0]:
                f = open('nutzer_info.txt', 'ab')
                f.write(verschluesseln(line))
                f.close()
                f = open('nutzer_info.txt', 'a')
                f.write("\n")
                f.close()
            else:
                f = open('nutzer_info.txt', 'ab')
                f.write(verschluesseln(userdaten[0] + " " + username + " " + code + " " +  userdaten[3]))
                f.close()
                f = open('nutzer_info.txt', 'a')
                f.write("\n")
                f.close()
                
        f.close()
    else:
        print("Titel ist nicht vorhanden.")

# löscht die datei mit dem übergebenem Dateinamen
def loesche_datei(dateiname):
    open(dateiname, 'w').close()

# verschlüsselt die Daten der Datei mit dem neuen crypter
def datei_neu_verschluesseln(altes_master, neues_master, dateiname):

    crypter_erstellen(altes_master)
    f = open(dateiname, 'rb')
    lines = f.readlines()

    daten = []

    for bit_line in lines:
        daten.append(str(entschluesseln(bit_line)))
    f.close()

    crypter_erstellen(neues_master)
    loesche_datei(dateiname)
    
    for datei in daten:
        f = open(dateiname, 'ab')
        f.write(verschluesseln(datei))
        f.close()
        f = open(dateiname, 'a')
        f.write("\n")
        f.close()

# das Masterpasswort wird geändert
def masterpasswort_aendern():

    altes_mpasswort = getpass.getpass("Bitte altes Masterpasswort eingeben: ")

    if passwort_pruefung(altes_mpasswort) == True:
        eingabe1 = getpass.getpass("Bitte gib dein Neues Masterpasswort ein: ")
        eingabe2 = getpass.getpass("Bitte gib dein Neues Masterpasswort erneut ein:")
        if eingabe1 == eingabe2:
            datei_neu_verschluesseln(altes_mpasswort, eingabe2, 'master_info.txt')
            datei_neu_verschluesseln(altes_mpasswort, eingabe2, 'nutzer_info.txt')
            time.sleep(0.2)
        
        else:
            print("Masterpasswort konnte nicht geändert werden!\n")


# Eine Zahlenfolge wird in einer Datei gespeichert
def speicher_verschluesselte_nummer():
    f = open('master_info.txt','ab')
    f.write(verschluesseln("12345"))
    f.close()

    f = open('master_info.txt','a')
    f.write("\n")
    f.close()

#prüft ob ein Masterpasswort vorhanden ist
def master_vorhanden():
    if os.stat("master_info.txt").st_size == 0:
        return False

    return True

#ein Masterpasswort wird erstellt
def mpasswort_erstellen():
    
    while (master_vorhanden() == False):
        print("Sie müssen ein Masterpasswort erstellen!")
        time.sleep(1)
        #getpass um Eingabe zu verbergen
        eingabe1 = getpass.getpass("Bitte geben Sie das gewünschte Masterpasswort ein: ")
        eingabe2 = getpass.getpass("Bitte Masterpasswort erneut eingeben: ")
    
        #falls Eingaben übereinstimmen springen wir aus dieser schleife aus und das passwort wird akzeptiert
        if eingabe1 == eingabe2:
            crypter_erstellen(eingabe2)
            speicher_verschluesselte_nummer()

        #falls Eingaben nicht übereinstimmen wiederholt sich der Prozess
        else:
            print("Passwörter stimmen nicht überein!\n")

# prüft ob das übergebene Passwort Kleinbuchstaben enthält
def check_kleinbuchstaben(passwort):
    for b in passwort:
        if b in string.ascii_lowercase:
            return True
    return False

# prüft ob das übergebene Passwort Großbuchstaben enthält
def check_grossbuchstaben(passwort):
    for b in passwort:
        if b in string.ascii_uppercase:
            return True
    return False

# prüft ob das übergebene Passwort Zahlen enthält
def check_zahlen(passwort):
    for b in passwort:
        if b in string.digits:
            return True
    return False

# prüft ob das übergebene Passwort Sonderzeichen enthält
def check_sonderzeichen(passwort):
    for b in passwort:
        if b not in string.digits and b not in string.ascii_lowercase and  b not in string.ascii_uppercase:
            return True
    return False

# gibt die Passwortstärke in "*" zurück
def passwortsicherheit(passwort):
    staerke = ""
    # prüft welche sicherheitsstufe erreicht wurde
    if check_grossbuchstaben(passwort) or check_kleinbuchstaben(passwort):
        staerke += "*"
    if check_zahlen(passwort):
        staerke += "*"
    if check_sonderzeichen(passwort):
        staerke += "*"

    # jenach stärke wird die Farbe der "*" angepasst
    if staerke == "*":
            print("Passwortstärke: "+ Fore.LIGHTRED_EX + staerke + Fore.RESET)

    elif staerke == "**":
            print("Passwortstärke: "+ Fore.LIGHTYELLOW_EX + staerke + Fore.RESET)

    elif staerke == "***":
            print("Passwortstärke: "+ Fore.LIGHTGREEN_EX + staerke + Fore.RESET)

# erstellt eine Textdatei
def datei_erstellen():
    f= open('nutzer_info.txt','a')
    f.close()
    f= open('master_info.txt', 'a')
    f.close()

akt_zeit_master = None
schlusszeit_zeit_master = time.time() +1000
befehl = ""
mpasswort = ""
versuche = 0

datei_erstellen()
nutzerdaten1 = Nutzerdaten()

#Falls kein Masterpassword vorhanden ist, wird eins erstellt 
mpasswort_erstellen()
#Der Nutzer hat 3 Versuche das Masterpassword einzugeben um fortzufahren
while master_vorhanden() and befehl != "exit":
    time.sleep(0.2)
    mpasswort = getpass.getpass("Bitte Masterpasswort eingeben um fortzufahren: ")
    versuche = versuche + 1
    crypter_erstellen(mpasswort)
    
    #wenn Masterpasswort übereinstimmt werden die Versuche auf 0 gesetzt
    if passwort_pruefung(mpasswort):
        versuche = 0
        #Eingabezeitpunkt und Ablaufzeitpunkt des Masterpasswortes speichern
        akt_zeit_master = time.time()
        schlusszeit_zeit_master = akt_zeit_master + 30
        befehl = ""
        print("Masterpasswort akzeptiert.")
        #Solang nicht der befehl nicht exit ist
        while befehl != "abgelaufen" and befehl != "exit":
            #Wenn das Masterpasswort abgelaufen ist wird der befehl zu exit und mpasswort ist nicht mehr das Masterpasswort
            if time.time() > schlusszeit_zeit_master:
                befehl = "abgelaufen"
                
            #Falls Masterpasswort gültig ist wird auf ein befehl gewartet
            else:
                befehl = input()
            #wenn der befehl generate ausgeführt werden soll, wird ein Passwort wird generiert
            if befehl =='generate':
                password_generator()

            elif befehl == 'store':
            #eingabe von titel username und passwort
                nutzerdaten1.title = input("Geben Sie den Titel ein: ")
                if exist(nutzerdaten1.title) == False:

                    nutzerdaten1.username = input("Geben Sie den Username ein: ")
                    nutzerdaten1.code = str(getpass.getpass("Geben Sie das Passwort: "))
                    passwortsicherheit(nutzerdaten1.code)
                    nutzerdaten1.daten_hinzufuegen()
                else:
                    print("Titel ist schon vorhanden.")

            elif befehl == "delete":
                nutzerdatei_loeschen()
                
            elif befehl == "modify":
                nutzerdatei_aendern()

            elif befehl == "list":
                nutzerdaten1.ganze_Liste_ausgeben()

            elif befehl == "search":
                nutzerdatei_finden()

            elif befehl == "change":
                masterpasswort_aendern()

            elif befehl == "check":
                pruefe_abgelaufene_passwoerter()           
                
    # Bei 3 Fehlversuchen wird das Programm beendet
    elif(versuche == 3):
        print("Programm beendet !")
        break