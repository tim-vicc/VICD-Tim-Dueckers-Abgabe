#importiert und erstellt blueprint
from flask import Blueprint
bp = Blueprint("workplace", __name__)
from app.workplace import routes  
