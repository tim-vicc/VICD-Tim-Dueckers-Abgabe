import datetime
from flask_login import FlaskLoginClient
from app.models import User, workplacedesk, Reservation
import pytest
from app import create_app, db
from tests.testconf import TestConfig

# Erstellt die Applikationskonfiguration für das Testing
@pytest.fixture
def testApp():
    app = create_app(TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        # erstellt die Arbeitsplätze
        for x in range(1, 10):
            desk = workplacedesk(id=x, price=5, info=f"desk {x}")
            db.session.add(desk)
        db.session.commit()
        #erstellt den Testbenutzer
        u = User(username="test") 
        u.set_password("test")
        db.session.add(u)
        db.session.commit()
        # Erstellt die Testreservation
        today = datetime.date.today()
        r = Reservation(user_id=u.id, workplace_desk_id=1, date=today)
        db.session.add(r)
        db.session.commit()
     # erstellt für den Folgetag eine Reservation
        tomorrow = today + datetime.timedelta(days=1)
        r2 = Reservation(user_id=u.id, workplace_desk_id=2, date=tomorrow)
        db.session.add(r2)
        db.session.commit()
        # Datenbereinigung  der DB
        yield app
        db.session.remove()
        db.drop_all()

# Tests mit authentifiziertem User
@pytest.fixture
def client(testApp):
    user = User.query.filter_by(username="tim").first()
    return testApp.test_client(user=user)

# Erstellt Token für den User
@pytest.fixture
def token(client):
    credentials = ("tim", "tim")
    tokenResponse = client.post(
        "api/tokens",
        auth=credentials,
    )
    token = tokenResponse.json["token"]
    return token

# überprüft den Token
class Testreservationsuebersicht:
    @pytest.mark.dependency()
    def test_token_get(self, token): 
        assert token is not None
#Ruft die Infromationen der Reservationsübersicht ab
    @pytest.mark.dependency(depends=["Testreservationsuebersicht::test_token_get"])
    def test_accountint_calc(self, client, token): 
  
        with client:
            response = client.get(
                "/api/reservationsuebersicht", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200

            data = response.json
            assert data["desks"] == 3
            assert data["occupied"] == 1
            assert data["occupation"] == 0.33
            assert data["revenue"] == 5
