#importiert div. Flaskmodule , blueprints , Login und logout module, User, DB und die Forms
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db

#überprüfung ob Benutzer bereits authentifiziert ist und leitet diesen ggf weiter auf die Reservationsseite
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  
        flash("Bereits eingeloggt")
        return redirect(url_for("workplace.index"))
#Anmeldeformular wird erstellt und das Loginformular
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Ungültiger Benutzername oder Passwort", "Fehler")
            return redirect(url_for("auth.login"))
        login_user(user)
        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("workplace.index")
        return redirect(next)
    return render_template("pages/login.html", title="Login", form=form)

#definiert das Userlogout
@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("workplace.index"))

# Das Registrierungsformular wird erstellt und prüft die Eingaben, bei erfolg wird auf das Login weitergeleitet
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:  
        return redirect(url_for("workplace.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data) 
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Benutzer {form.username.data} wurde erstellt")
        return redirect(url_for("auth.login"))
    return render_template("pages/register.html", title="Registrieren", form=form)
