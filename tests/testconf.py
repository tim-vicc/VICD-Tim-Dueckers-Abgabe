import pytest
from app import create_app, db
from config import Config

# Klasse zur Konfiguration der Testumgebung und erbt daten aus der Config für den Normalbetrieb
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
# Erstellt die Applikation für die Testfälle
@pytest.fixture
def fixture():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        #Bereinigt die Datenbank
        yield app
        db.session.remove()
        db.drop_all()
# der Test_client  wird zur Verfügung gestellt
@pytest.fixture
def client(app):
    return app.test_client()
