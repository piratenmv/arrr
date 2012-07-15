Das Arrr zum Sonntag
====================

Was ist das hier?
-----------------

Der Landesverband Mecklenburg-Vorpommern der Piratenpartei (http://piratenpartei-mv.de) verschickt seit einigen Monaten wöchentlich einen Newsletter an Neumitglieder - das "Arrr zum Sonntag". Es ist kein Newsletter im klassischen Sinne, bei dem einfach jede Woche eine Mail an alle verschickt wird. Es ist vielmehr ein personalisierter Newsletter, bei dem jedes Mitglied eine Reihe von Mails in einer festen Reihenfolge bekommt.

Beispiel:

- Fr, 30.03.2012: Andrea tritt in die Piratenpartei ein
- So, 01.04.2012: Andrea bekommt die 1. Ausgabe des "Arrr zum Sonntag"
- Di, 03.04.2012: Bert tritt in die Piratenpartei ein
- So, 08.04.2012: Bert bekommt die 1. und Andrea bekommt die 2. Ausgabe des Arrr zum Sonntag

und so weiter.

Das Ziel dabei soll sein, die Piraten nach und nach an die Piratenpartei heranzuführen und die üblichen FAQs in verdaulichen Happen Sonntag für Sonntag zu verteilen. Nebenbei enthält das "Arrr zum Sonntag" eine Wochenvorschau mit Stammtisch-Terminen etc.


Vorbereitung
------------

Um das "Arrr zum Sonntag" auszuprobieren, müssen zunächst in der Datei `config.json` Informationen zu einem SMTP-Server, dem Absender und dem Betreff der Mail eingetragen werden:

    {
      "smtp": {
        "server": "smtp.piraten-mv.de",
        "port": 25,
        "username": "superadmin",
        "password": "vollg3h3im"
      },
      "subject": "Das Arrr zum Sonntag",
      "sender": {
        "name": "Piraten MV Mitgliederbetreuung",
        "address": "mitglieder@piraten-mv.de"
      }
    }

Als nächstes müssen in die Datei `user.json` die Adressen der glücklichen Neupiraten eingetragen werden:

    [
        {
            "address": "andrea@inter.net", 
            "name": "Andrea"
        }
    ]

Fertig!

Nun kann mit

    ./arrr.py

die erste Runde Mails verschickt werden. In der Datei `user.json` wird nun pro Pirat vermerkt, welche Mails wann verschickt wurden und welche Mail die nächste ist.

    [
        {
            "address": "andrea@inter.net", 
            "history": {
                "1": "Sun Jul 15 22:26:49 2012"
            }, 
            "mailnumber": 2, 
            "name": "Andrea"
        }
    ]


Anpassen
--------

Die verschickten Mails liegen im Ordner `mails`. Da ist einmal die Datei `header.txt`, die die Anrede enthält. Das Feld `{name}` wird vom Script durch den `name`-Eintrag der Datei `user.json` ersetzt. Die Datei `footer.txt` enthält die Signatur und Informationen zum Abbestellen des Newsletters. Die Mails `mail1.txt`, `mail2.txt`, usw. sind die eigentlichen Mails. Eine Anzahl ist nicht vorgegeben: solange noch ungesendete Mails existieren, wird weiter geschickt. Innerhalb der Mails gibt es ein Feld `{calendarentries}`, das mit den Kalendereinträgen der nächsten Woche ersetzt wird.

Wenn man ohne den Kalender leben kann, sollte eine Anpassung ganz einfach sein: die Dateien in `mails` anpassen (nicht vergessen, in `config.json` den Betreff zu ändern!) und gut.


Voraussetzungen
---------------

- Wir nutzen die URL http://opendata.piratenpartei-mv.de/calendar um Kalenderdaten für die nächste Woche zu bekommen. Der Quelltext dazu wird hoffentlich bald unter https://github.com/piratenmv/opendata veröffentlicht.
- Das Paket "python-dateutil 2.1" (http://pypi.python.org/pypi/python-dateutil/) wird benötigt um die Kalenderdaten zu zähmen.


Fragen
------

Bei Fragen bitte eine Mail an support@piraten-mv.de schreiben. Wir helfen gerne!