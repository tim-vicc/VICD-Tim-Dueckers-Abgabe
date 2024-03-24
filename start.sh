#!/bin/bash
source /test/abgabe-vicd/venv/bin/activate
exec gunicorn -w 4 -b 0.0.0.0:5000 workplace:app
