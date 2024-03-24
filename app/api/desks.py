#importieren der benötigten Flaskmodule, models, Blueprint und die Token authentifizierung
import datetime
from flask import jsonify, abort
from app.models import workplacedesk
from app.api import bp
from app.api.auth import token_auth

# Gibt die Informationen zu einem Arbeitsplatz aus aufugrund der ID
@bp.route("/desks/<int:id>", methods=["GET"])
@token_auth.login_required
def get_desk(id):


    return jsonify(workplacedesk.query.get_or_404(id).to_dict())

# Überprüft den Reservationsstatus
@bp.route("/desks", methods=["GET"])
def get_desks():

    data = workplacedesk.to_collection_dict(workplacedesk.query)
    return jsonify(data)


@bp.route("/desks/<int:id>/get_desk_reservations", methods=["GET"])
@token_auth.login_required
def get_desk_reservations(id):

    desk = workplacedesk.query.get_or_404(id)
    data = workplacedesk.to_collection_dict(desk.reservations)
    return jsonify(data)

#überprüft Reservationsstatus an entsprechendem Datum
@bp.route("/desks/<int:id>/get_desk_reserved/<date>", methods=["GET"])
@token_auth.login_required
def get_desk_reserved(id, date):

    #Fehlerbehandlung bei Datum zu Objekt Umwandlung
    try:
        dateObj = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)
# Rückgabewert Ture oder False je nach Reservationsstatus
    desk = workplacedesk.query.get_or_404(id)
    reservation = desk.is_reserved(dateObj)
    if reservation:
        return jsonify(True)
    return jsonify(False)
