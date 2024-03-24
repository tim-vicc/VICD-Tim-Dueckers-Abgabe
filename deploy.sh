#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker build -t app-db .
docker run -d --name sql-container -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword app-db
docker start sql-container
gunicorn -w 4 -b 0.0.0.0:5000 workplace:app &
