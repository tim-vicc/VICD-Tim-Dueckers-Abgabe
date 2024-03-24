import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apidoc import ApiDoc
from sqlalchemy import select
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"  
doc = ApiDoc()

#erstellt die Python-Flask-Anwendung
def create_app(config=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    from app import models
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.workplace import bp as workplace_bp
    app.register_blueprint(workplace_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    doc.init_app(app)
    
    #die Log Kanäle werden definiert und wohin die Logs geschrieben werden sollen. zudem wird zwischen debug mode, testing mode und normal unterschieden
    if not app.debug and not app.testing:
        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/workplace.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("App startup")

 #hier wird nur zwischen dem testing mode und dem Rest unterschieden um die DB entsprechend abfüllen zu können
    if not app.testing:
        with app.app_context():
            
            db.create_all()
            if not db.session.execute(select(models.workplacedesk)).first():
                # Erstellen der Arbeitsplätze falls noch nicht vorhanden. Hier wird die Anzahl und der Preis für eine Reservation festgelegt
                for x in range(1, 41):
                    desk = models.workplacedesk(id=x, price=5, info=f"desk {x}")
                    db.session.add(desk)
                db.session.commit()
    # Wiedergabe der konfigurierten Anwendung
    return app
#Teilweise generiert, vsc cody
