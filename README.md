Nachfolgend wird beschrieben wie das Projekt als Testumgebung installiert werden kann. Gegebenenfalls sollte die IP in der Applikation angepasst werden.

Um dieses Projekt manuell zu deployen und starten folgende Schritte ausführen:
1. git clone "gitrepo"
2. wechseln in das geklonte git repo
3. python3 -m venv .venv - Erstellung einer virtuellen Python-Umgebung.
4. source .venv/bin/activate - Aktivierung der zuvor erstellten virtuellen Umgebung.
5. pip install -r requirements.txt - Installation der Abhängigkeiten aus der Datei `requirements.txt`.
6. docker build -t <image-name> <ziel_dir>
7. docker run -d --name <sql-container-name>-p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword <image-name>
8. docker start <sql-container-name>
9. flask run --host=0.0.0.0 oder gunicorn -w 4 -b 0.0.0.0:5000 workplace:app

Um dieses Projekt automatisch zu deployen 
1. ggf dploy.sh ausführbar machen
2. ./deploy.sh

Um dieses Projekt zu starten:
1. ggf start.sh ausführbar machen
2. start.sh ausführen

Um den Code automatisch zu aktualisieren nachdem änderungen an dem Repository vorgenommen wurden:
1. überprüfen des dockercontainer namens und ggf. script anpassen.
2. ./update.sh          - ausführen des updates
   
