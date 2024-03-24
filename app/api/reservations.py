# importieren von jsonify, den models, blueprints und der authentifizierung mittels token
from flask import jsonify
from app.models import Reservation, workplacedesk, User
from app.api import bp
from app.api.auth import token_auth

# Token authentifizierung wird geprüft und gibt Informationen zu einer Reservation zurück.
@bp.route("/reservations/<int:id>", methods=["GET"])
@token_auth.login_required
def get_reservation(id):
    #Abfüllen der Parameter für Fehlermeldung
    return jsonify(Reservation.query.get_or_404(id).to_dict())

#Fragt alle Reservationen ab
@bp.route("/reservations", methods=["GET"])
def get_reservations():
    #Automatische API Beschreibung mit Beispielen (AUS APIDOC)

    data = Reservation.to_collection_dict(Reservation.query)
    return jsonify(data)

# Listet alle Benutzerspeziofischen Informationen der Reservationen und überprüft ebenfalls die Authentifizierung
@bp.route("/reservations/<int:id>/get_reservation_user", methods=["GET"])
@token_auth.login_required
def get_reservation_user(id):

    #Errorhandliung
    reservation = Reservation.query.get_or_404(id)
    user = User.query.get_or_404(reservation.user_id)
    return jsonify(user.to_dict())

#überprüft die Authemtifizierung und gibt Informationen zu einer Reservation aus anhand der ID
@bp.route("/reservations/<int:id>/get_reservation_desk", methods=["GET"])
@token_auth.login_required
def get_reservation_desk(id):

    reservation = Reservation.query.get_or_404(id)
    desk = workplacedesk.query.get_or_404(reservation.workplace_desk_id)
    return jsonify(desk.to_dict())
