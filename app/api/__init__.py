from flask import Blueprint
# Erstellt den Blueprint api für div. gruppen mittels vorher importiertem Flaskmodul
bp = Blueprint("api", __name__)

from app.api import tokens, errors, desks, reservationsuebersicht, reservations  
