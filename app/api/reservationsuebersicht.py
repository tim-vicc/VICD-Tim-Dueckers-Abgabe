#Import der Module für Datim, jsonify, Select für die DB Abfragen, die benötigten Models, Blueprint, Datenbank und Authentifizierung
import datetime
from flask import jsonify
from sqlalchemy import select
from app.models import Reservation, workplacedesk, User
from app.api import bp
from app.api.auth import token_auth
from app import db

#Überprüft die Authentifizierung, 
@bp.route("/reservationsuebersicht", methods=["GET"])
@token_auth.login_required
def get_reservationsuebersicht():

    #Ruft entsprechende Infromationen aus der Datenbank ab für die statischen Werte
    desks = db.session.scalars(select(workplacedesk)).all()
    deskCount = len(list(desks))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), desks)))
    occupation = round((occupied / deskCount), 2)
    #ruft die Reservatrionen ab und deren zugehörigen Informationen wie den Benutzer und das Datum. Filtert die Reservationen ebenfalls nach dem aktuellen Datm
    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(workplacedesk)
        .join(User)
    ).all()
    #Die gesammelten Daten werden entsprechend ausgegeben 
    revenue = sum(map(lambda x: x.workplace_desk.price, reservations))
    return jsonify(
        {
            "desks": deskCount,
            "occupied": occupied,
            "occupation": occupation,
            "revenue": revenue,
        }
    )

