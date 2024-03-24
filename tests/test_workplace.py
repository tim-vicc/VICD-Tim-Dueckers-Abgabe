import datetime

from app.models import Reservation, User, workplacedesk
import pytest
from app import create_app, db
from tests.testconf import TestConfig
from flask_login import FlaskLoginClient

# Erestellt die Konfiguration der Applikation für das Testing
@pytest.fixture
def testApp():
    app = create_app(TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        # Create default workplace desks
        for x in range(1, 10):
            desk = workplacedesk(id=x, price=5, info=f"desk {x}")
            db.session.add(desk)
        db.session.commit()

        u = User(username="tim")  # type: ignore
        u.set_password("tim")
        db.session.add(u)
        db.session.commit()
        # Datenbereinigung in der DB
        yield app
        db.session.remove()
        db.drop_all()

#testing mit authentifiziertem User
@pytest.fixture
def client(testApp):
    user = User.query.filter_by(username="tim").first()
    return testApp.test_client(user=user)

# testet das Reservationsmodel
class Testworkplace:
    @pytest.mark.dependency()
    def test_reserve_model(self, testApp):  
        today = datetime.date.today()
        desk = workplacedesk.query.filter_by(id=1).first()
        desk.reserve(today, User.query.filter_by(username="susan").first())
        assert desk.is_reserved(today)
#testet das model zur Freigabe des platzes
    @pytest.mark.dependency()
    def test_free_model(self, testApp): 
        today = datetime.date.today()
        desk = workplacedesk.query.filter_by(id=1).first()
        desk.reserve(today, User.query.filter_by(username="susan").first())
        userReservation = desk.free(
            today, User.query.filter_by(username="susan").first()
        )

        assert userReservation is not None

    @pytest.mark.dependency(
        depends=[
            "Testworkplace::test_reserve_model",
            "Testworkplace::test_free_model",
        ]

    #testet route zur reservation
    )
    def test_reserve_route(self, client, testApp):
        today = datetime.date.today()
        with client:
            response = client.post(f"/reserve/1/{today.isoformat()}")
        assert response.status_code == 302
        with testApp.app_context():
            assert Reservation.query.filter_by(date=today).first() is not None

    @pytest.mark.dependency(
        depends=[
            "Testworkplace::test_reserve_model",
            "Testworkplace::test_free_model",
            "Testworkplace::test_reserve_route",
        ]
    )
    # testet die Route um eine Reservation aufzuheben
    def test_free_route(self, client, testApp):
        """Integration Test freeing a desk through the route"""
        today = datetime.date.today()
        with client:
            response = client.post(f"/reserve/1/{today.isoformat()}")
        with testApp.app_context():
            assert Reservation.query.filter_by(date=today).first() is not None

        with client:
            response = client.post(f"/free/1/{today.isoformat()}")
        assert response.status_code == 302
        with testApp.app_context():
            assert Reservation.query.filter_by(date=today).first() is None
