from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import select
from app.models import workplacedesk, Reservation, User
from app import db
from app.workplace import bp
from app.workplace.calendar import workplaceCalendar
from app.workplace.forms import BaseForm
import datetime
# Erstellt eine Kalenderinstanz 
Calendar = workplaceCalendar()

# zeigt die Reservatiosseite an, prüft auf eine valide Authentifizierung
@bp.route("/")
@login_required
def index():
    form = BaseForm()
#schreibt das aktuelle Datum in die entsprechenden Variabeln
    year = datetime.date.today().year
    month = datetime.date.today().month
    today = datetime.date.today()
# wählt alle Arbeitsplätze aus der Datenbank und schreibt diese in desks
    desks = db.session.scalars(select(workplacedesk))
# gibt die Daten in das Rendering template aus
    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        activeDate=today,
        today=today,
        weeks=Calendar.get_days(month, year),
        desks=desks,
        form=form,
    )

# Zeigt die Reservationsseite entsprechend des Datums an, z.b um Buttons entsprechend des Statuses anzuzeigen. inkl. fehlerhandling
@bp.route("/workplace/<date>")
@login_required
def date(date):
    form = BaseForm()
    try:
        activeDate = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    today = datetime.date.today()
    if activeDate < today:
        abort(404)

    year = datetime.date.today().year
    month = datetime.date.today().month
    desks = db.session.scalars(select(workplacedesk))
#Gibt die zuvor abgefragten daten aus
    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        today=today,
        activeDate=activeDate,
        weeks=Calendar.get_days(month, year),
        desks=desks,
        form=form,
    )

# Reservation auf bestimmtes Datum mit Fehlerhandling
@bp.route("/reserve/<desk>/<day>", methods=["POST"])
@login_required
def reserve(desk, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Reservationen in der Vergangenheit sind nicht möglich")
            return redirect(url_for("workplace.index"))
            
        desk = workplacedesk.query.filter_by(id=desk).first()
        if desk is None:
            flash(f"desk {desk} not found.")
            return redirect(url_for("workplace.index"))

        user = User.query.filter_by(id=current_user.id).first()  
        if user is None:
            raise ValueError("User not found")

        if user.reservation(dayDate):
            flash(
                "Cannot reserve desk. You can only have 1 reservaton per day", "error"
            )
            return redirect(url_for("workplace.index"))

        desk.reserve(dayDate, current_user)
        flash(f"desk {desk} reserved!")
        db.session.commit()
#Rückkehr auf die Reservationsseite
        return redirect(url_for("workplace.index"))
    else:
        return redirect(url_for("workplace.index"))

#Aufheben der Reservation
@bp.route("/free/<desk>/<day>", methods=["POST"])
@login_required
def free(desk, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Reservationen aus der Vergangenheit können nicht bearbeitet werden")
            return redirect(url_for("workplace.index"))

        desk = workplacedesk.query.filter_by(id=desk).first()
        if desk is None:
            flash(f"desk {desk} not found.")
            return redirect(url_for("workplace.index"))

        userReservation = desk.free(dayDate, current_user)
        if userReservation is not None:
            db.session.delete(userReservation)
            db.session.commit()
            flash(f"desk {desk} wurde freigegeben")
        else:
            flash(f"desk {desk} wurde durch jemand anderes reserviert.", "error")
#zurück auif die reservationsseite
        return redirect(url_for("workplace.index"))
    else:
        return redirect(url_for("workplace.index"))


@bp.route("/reservationsuebersicht")
@login_required
def reservationsuebersicht():
    # prüft, ob der User ein Admin ist und zeigt entsprechend alle Reservationen an
    if current_user.username != "admin":
        print("User is not admin")

    desks = db.session.scalars(select(workplacedesk)).all()
    deskCount = len(list(desks))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), desks)))
    occupation = round((occupied / deskCount) * 100)

    # if user is not admin, filter reservations by user
    if current_user.username != "admin":
        reservations = db.session.scalars(
            select(Reservation)
    #        .filter(Reservation.date <= today)
            .join(workplacedesk)
            .join(User)
            .filter(User.id == current_user.id)
        ).all()

    #Ist der User nicht gleich "admin" zeigt es nur die eigenen Reservationen an
    else:
        reservations = db.session.scalars(
            select(Reservation)
 #           .filter(Reservation.date <= today)
            .join(workplacedesk)
            .join(User)
        ).all()
# Summiert die Reservationskosten
    revenue = sum(map(lambda x: x.workplace_desk.price, reservations))
# gibt die zuvor bestimmten Daten wieder
    return render_template(
        "pages/reservationsuebersicht.html",
        title="reservationsuebersicht",
        desks=deskCount,
        occupied=occupied,
        occupation=occupation,
        reservations=reservations,
        revenue=revenue,
    )
#Teilweise generiert, vsc cody
