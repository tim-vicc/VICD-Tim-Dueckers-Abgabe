#Import von jsonify und den HTTP Statuscodes
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# Fehlermeldung im Falle eines error 400
def bad_request(message):
    # Ausgabe der Fehlermeldung)
    return error_response(400, message)

#Fehlermeldung im Falle einer unbekannten Fehlermeldung
def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    # Erestellt die Antwort anhand der vorherigen nachricht und gibt diese aus
    response = jsonify(payload)
    response.status_code = status_code
    return response
