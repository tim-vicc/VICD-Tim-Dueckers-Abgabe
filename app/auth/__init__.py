from flask import Blueprint
#Importiert das Blueprint moduzl von flask und der auht blueprint wird erstellt
bp = Blueprint("auth", __name__)
from app.auth import routes  
