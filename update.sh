#!/bin/bash

# Zurücksetzen lokaler Änderungen und Aktualisieren des Codes
git reset --hard HEAD
git checkout .
git clean -fd
git_pull_output=$(git pull)

# Überprüfen, ob Änderungen vorhanden sind
if echo "$git_pull_output" | grep -q "Already up to date."; then
    echo "Keine Änderungen gefunden. Skript wird beendet."
    exit 0
fi

# Aktivieren der Virtualenv-Umgebung
source .venv/bin/activate

# Installieren der Abhängigkeiten
pip install -r requirements.txt

# Alte Container stoppen und entfernen
docker ps -a | grep 'sql-container' | awk '{print $1}' | xargs -r docker stop | xargs -r docker rm

# Alte Images entfernen
docker images | grep 'app-db' | awk '{print $3}' | xargs -r docker rmi

# Automatische Versionierung für das Docker-Image
version=$(date +%Y%m%d%H%M)
image_name="app-db:$version"
container_name="sql-container-$version"

# Erstellen des Docker-Images
docker build -t $image_name .

# Starten des Docker-Containers
docker run -d --name $container_name -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword $image_name

# Überprüfen, ob der Container läuft, und Starten, falls nicht
if ! docker ps | grep -q $container_name; then
    docker start $container_name
fi

# Starten der Flask-Applikation
gunicorn -w 4 -b 0.0.0.0:5000 workplace:app &

