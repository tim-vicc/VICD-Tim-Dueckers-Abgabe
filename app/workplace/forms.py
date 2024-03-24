#importiert und erstellt eine Klasse für die Formulare
from flask_wtf import FlaskForm
from wtforms import SubmitField
class BaseForm(FlaskForm):
    submit = SubmitField("Submit", render_kw={"class": "btn btn-neutral"})
