import base64
import os
from datetime import datetime, timedelta
from flask import url_for
from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

#erstellt ein Wörterbuch der SQL Alchemy Query in dem die Einträge gelistet werden
class CollectionMixin(object):
    @staticmethod
    def to_collection_dict(query):
        resources = query.all()
        data = {
            "items": [item.to_dict() for item in resources],
        }
        return data

# Erstellt das Benutzermodel  und erbt entsprechende Daten von UserMixin und vom db.model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship("Reservation", backref="user", lazy="dynamic")
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
# zur sicherheit wird das Passwort als Hash gespeichert und nicht als klartext
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
# überprüft den hash des Passworts
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#Generiert und speichert einen Token für den User falls nicht vorhanden oder erneuert einen bestehenden
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
# Token wird hiermit wiederrufen
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
# überprüft dern Token auf seine Gültigkeit
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
# überprüft die Reservation des Benutzers
    def reservation(self, date):
        return self.reservations.filter_by(date=date).first()
# Erstellt data mit dem inhalt id und username
    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
        }
        return data
# gibt das Objekt User als string wieder
    def __repr__(self):
        return f"<User {self.username}>"

# Lädt den Benutzer mittels seiner ID für das Flask Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Klasse fpr einen Arbeitsplatz
class workplacedesk(db.Model, CollectionMixin):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    info = db.Column(db.String(256))
    reservations = db.relationship(
        "Reservation", backref="workplace_desk", lazy="dynamic"
    )
# überprüft den Arbeitsplatz auf eine vorhandene reservation 
    def is_reserved(self, date):
        return self.reservations.filter_by(date=date).first()
# Reserviert den Platz mit den Angaben des users und Datum
    def reserve(self, date, user):
        if not self.is_reserved(date):
            self.reservations.append(Reservation(date=date, user=user))
#Gibt den Reservierten Arbeitsplatz frei
    def free(self, date, user):
        userReservation = self.reservations.filter_by(date=date, user=user).first()
        if userReservation:
            self.reservations.remove(userReservation)
            return userReservation
        else:
            return None
# Erstellt ein Wörterbuch mit den entsprechenden API einträgen
    def to_dict(self):
        data = {
            "id": self.id,
            "price": self.price,
            "info": self.info,
            "_links": {
                "self": url_for("api.get_desk", id=self.id),
                "reservations": url_for("api.get_desk_reservations", id=self.id),
                "reserved": url_for(
                    "api.get_desk_reserved", id=self.id, date="2024-01-01"
                ),
            },
        }
        return data
# Gibt das Arbeitsplkatzobjekt als String wieder
    def __repr__(self):
        return f"<workplacedesk {self.id}>"


class Reservation(db.Model, CollectionMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    workplace_desk_id = db.Column(db.Integer, db.ForeignKey("workplacedesk.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        data = {
            "id": self.id,
            "date": self.date,
            "workplace_desk_id": self.workplace_desk_id,
            "user_id": self.user_id,
            "_links": {
                "self": url_for("api.get_reservation", id=self.id),
                "user": url_for("api.get_reservation_user", id=self.id),
                "desk": url_for("api.get_reservation_desk", id=self.id),
            },
        }
        return data
# Gibt das Reservationsobjekt als String wieder 
    def __repr__(self):
        return f"<Reservation {self.id}>"
#Teilweise generiert, vsc cody
