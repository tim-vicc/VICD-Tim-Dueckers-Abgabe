#Importiert die Module Flaskform, module für die Eingabefelder bei Login etc. und das das User model
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User

#Definition des Loginformulars
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    submit = SubmitField(
        "Einloggen",
        render_kw={"class": "btn btn-primary"},
    )

#Definition des Registrierungsformulars
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "input input-bordered"},
    )
    password = PasswordField(
        "Passwort",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    passwordRepeat = PasswordField(
        "Passwort wiederholen",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "input input-bordered"},
    )
    submit = SubmitField(
        "Registrieren",
        render_kw={"class": "btn btn-primary"},
    )
#Validiert die Eingabe für den Benutzernamen aufgrund möglicher Redundanz, damit keine doppelten Namen entstehen
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValueError("Username bereits vergeben")
