# importieren des flask moduls
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
# importieren des User models und der error meldungen
from app.models import User
from app.api.errors import error_response

# Erstellt Instanzen zur Authentifizierung 
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

# Funktion zur verifizierung der Benutzerangaben. Es wird der Benutzer und dessenb Passwort abgefragt und bei korrektheit der Benutzer zurückegegeben
@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

# Funktion zur Überprüfung des Tokens
@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

# Funktionen  zum Fehlerhandling bei der Authentifizierung
@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
