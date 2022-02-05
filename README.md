# Fritz TR-064 (14102)

## Beschreibung 

Baustein zur Steuerung der FritzBox via TR-064, z.B. zur Konfiguration des WLAN.

Die TR-064 Schnittstelle muss über dir Fritz!Box Web-Oberfläche ggf. erst aktiviert werden:

1. Expertenansicht aktivieren
2. Heimnetz - Heimnetzübersicht - Netzwerkeinstellungen
3. Zugriff für Anwendungen zulassen aktivieren

AVM bietet unter der Rubrik <a href="https://avm.de/service/schnittstellen/">Schnittstellen</a> - Apps/TR-064 viele Informationen über die Möglichkeiten.</p>

### 2: Configuration WLAN

Zur Nummerierung der WLAN Eingänge aus der AVM Dokumentation:

*If the device supports WLAN one service is listed (service #1). If the device additionally supports a second physical access point support 2.4 GHz and 5 GHz, one more service is listed (service #2). If a third physical access point is supported, an additional service is listed (service #3).  If the device supports a logical Access Point for guests, one more service is listed (service #2, #3 or #4).*

### 3: Anwesenheitserkennung

Über die Ein-/Ausgänge kann für Geräte Anhand ihrer MAC Adresse festgestellt werden, ob sie an der Fritz!Box angemeldet sind.

### 4: Wählhilfe

Zur Nutzung der Anruf-Funktion muss die Wahlhilfe aktiviert sein (Telefonie - Anrufe - Wählhilfe). 
Die Anruffunktion stellt dabei eine Verbindung her, zwischen dem Telefon, welches unter "Wählhilfe" 
in der Fritz!Box-Oberfläche konfiguriert ist und der Nummer, die dem Baustein übergeben wird.

## Inputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Benutzer | | Benutzername eines Fritz!Box-Zugangs. |
| 2 | Passwort | | Passwort des Fritz!Box-Zugangs. |
| 3 | FritzBox IP | | <p>IP der FritzBox, mit der die TR-064 Kommunikation stattfinden soll.</p><p>Der Parameter ist optional. Ist er nicht angegeben, wird die FritzBox automatisch gesucht. Bei mehreren FritzBoxen im gleichen Netzwerk kann hierbei die falsche zur Kommunikation gewählt werden.</p><p>Der Wert wird ausschließlich bei der Initialisierung ausgelesen!</p> |
| 4 | WLAN 1 E/A | 0 | Ein-/Ausschalten (1/0) des WLAN-Signals. |
| 5 | WLAN 2 E/A | 0 | Ein-/Ausschalten (1/0) des WLAN-Signals. |
| 6 | WLAN 3 E/A | 0 | Ein-/Ausschalten (1/0) des WLAN-Signals. |
| 7 | Gast-WLAN E/A | 0 | Ein-/Ausschalten (1/0) des WLAN-Signals. |
| 8 | MAC-Addr 1 | | MAC-Adresse zur Anwesenheitserkennung. Die Anwesenheitsprüfung wird ausgeführt, wenn der Eingang geschrieben wird. Die MAC-Adresse muss im Format <code>ab:cd:ef:gh:ij:kl</code> angegeben werden. |
| 9 | MAC-Addr 2 | | MAC-Adresse zur Anwesenheitserkennung. Die Anwesenheitsprüfung wird ausgeführt, wenn der Eingang geschrieben wird. Die MAC-Adresse muss im Format <code>ab:cd:ef:gh:ij:kl</code> angegeben werden. |
| 10 | MAC-Addr 3 | | MAC-Adresse zur Anwesenheitserkennung. Die Anwesenheitsprüfung wird ausgeführt, wenn der Eingang geschrieben wird. Die MAC-Adresse muss im Format <code>ab:cd:ef:gh:ij:kl</code> angegeben werden. |
| 11 | MAC-Addr 4 | | MAC-Adresse zur Anwesenheitserkennung. Die Anwesenheitsprüfung wird ausgeführt, wenn der Eingang geschrieben wird. Die MAC-Adresse muss im Format <code>ab:cd:ef:gh:ij:kl</code> angegeben werden. |
| 12 | Rufnummer | 0 | Rufnummer, die gewählt werden soll. |
| 13 | Dial/Hang-Up (1/0) | 0 | Wählt die Nummer bei 1, beendet die Verbindung bei 0 |
| 14 | AB E/A | 0 | Anrufbeantworter 1 ein-/ausschalten (1/0) |
| 15 | Reboot | 0 | Löst bei eingehender 1 einen Reboot der Fritz!Box aus. |
| 16 | Gen. SOAP Aktion | | Über diesen Eingang können beliebige SOAP Aktionen an die Fritz!Box übermittelt werden.<br>Der Aktionsaufruf muss dabei wie folgt gebildet werden: <code>{"serviceType":"urn:dslforum-org:service:WLANConfiguration:1", "action_name":"SetEnable","argumentList":{"NewEnable":"1"}}</code><br>Da über den HS keine " eingegeben werden können, müssen diese html encodiert werden. Hierbei muss wie folgt ersetzt werden: " &ensp; = &ensp; <i>&#38;quot;</i>. |


## Ausgänge

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | RM WLAN 1 E/A | 0 | Rückmeldung des Ein-/Aus-Zustandes (1/0) des WLAN Signals. Hierzu wird der Status (Up/Deactivated) mit dem Enabled-Signal (1/0) kombiniert. |
| 2 | RM WLAN 2 E/A | 0 | Rückmeldung des Ein-/Aus-Zustandes (1/0) des WLAN Signals. Hierzu wird der Status (Up/Deactivated) mit dem Enabled-Signal (1/0) kombiniert. |
| 3 | RM WLAN 3 E/A | 0 | Rückmeldung des Ein-/Aus-Zustandes (1/0) des WLAN Signals. Hierzu wird der Status (Up/Deactivated) mit dem Enabled-Signal (1/0) kombiniert. |
| 4 | RM Gast-WLAN | 0 | Rückmeldung des Ein-/Aus-Zustandes (1/0) des WLAN Signals. Hierzu wird der Status (Up/Deactivated) mit dem Enabled-Signal (1/0) kombiniert. |
| 5 | SSID WLAN 1 | | SSID des WLAN Signals |
| 6 | SSID WLAN 2 | | SSID des WLAN Signals |
| 7 | SSID WLAN 3 |  | SSID des WLAN Signals |
| 8 | SSID Gast-WLAN | | SSID des WLAN Signals |
| 9 | MAC-Addr 1 angem. | 0 | 1 = Gerät anwesend ist,</br> 0 = Gerät nicht anwesend |
| 10 | MAC-Addr 2 angem. | 0 | 1 = Gerät anwesend ist,</br> 0 = Gerät nicht anwesend  |
| 11 | MAC-Addr 3 angem. | 0 | 1 = Gerät anwesend ist,</br> 0 = Gerät nicht anwesend  |
| 12 | MAC-Addr 4 angem. | 0 | 1 = Gerät anwesend ist,</br> 0 = Gerät nicht anwesend  |
| 13 | (Beliebiger) Gast angem. | 0 | 1 = Gast angemeldet,</br> 0 = Kein Gast angemeldet |
| 14 | AB E/A | 0 | Ein/aus-Status Anrufbeantworter 1 |
| 15 | Gen. Soap Antw. |  | Antwort auf die generische Anfrage |

## Sonstiges

- Neuberechnung beim Start: Nein
- Baustein ist remanent: Nein
- Baustein Id: 14102
- Kategorie: Datenaustausch

### Change Log

- v1.03
    - Impr.: Debug ausgaben & Stabilität durch try-catch bei regelm. Statusabfrage
- v1.02
    - Fix: JSON Ausgabe der SOPA-Antwort mit " statt '
- v1.01
    - tbd
- v1.00
    - Impr.: Neuer Ausgang: Gerät im Gast-WLAN angemeldet
    - Impr.: Debug-Ausgaben plotten jew. IP mit
- v0.8
    - Impr.: WLAN Status nutzt nur noch "NewStatus" und nicht mehr "NewEnable" UND "NewStatus"
- v0.7
    - Impr.: Optionale Eingabe der FritzBox IP
- v0.6
    - Impr.: Ein-/Ausgang zum AB
    - Impr.: Eingang zum Reboot der Fritz!Box
    - Fix: Baustein bleibt bei fehlender Verbindung zur FritzBox hängen; Timeout nach 3s für Kommunikation eingefügt
- v0.5
    - Impr.: Baustein erkennt HS-IP selbständig
- v0.4
    - Timer zur Intervall-Abfrage des Status
    - Ein-/Ausgänge für generische SOAP Requests
    - Fix: Bei unter 4 WLAN Signalen wird der Status des Gast-WLAN nicht auf dem Ausgang Gast-WLAN ausgegeben, sondern nur auf dem höchsten Index, z.B. WLAN 3
- v0.3
    - Fix: RM WLAN 2 wird auf WLAN 3 ausgegeben
    - Fix: Gast-WLAN E/A setzt WLAN 1
- v0.2
    - Anwesenheitserkennung
    - Wählhilfe
    - Automatische Erkennung Gast-WLAN
- v0.1
    - Initiales Release

### Open Issues / Know Bugs

- none

### Support

Please use [github issue feature](https://github.com/En3rGy/14102_FritzBox_TR-064/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.


### Code

Der Python-Code des Bausteins befindet sich in der hslz Datei oder auf [github](https://github.com/En3rGy/14102_FritzBox_TR-064).

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)


## Requirements

x

## Software Design Description

### Definitions

x

### Solution Outline

x

## Validation & Verification

x

## Licence

Copyright 2021 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

