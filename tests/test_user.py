from app.models import User
import pytest
from tests.testconf import TestConfig  # noqa: F401
from app import create_app, db


@pytest.fixture
def testApp():
    # Start setup, create new app and database
    app = create_app(TestConfig)
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(testApp):
    return testApp.test_client()


class TestUser:
    @pytest.mark.dependency()
    def test_password_hashing(self, testApp):  # noqa: F811
        """Unit Test hashing of password"""
        u = User(username="Tim")  # type: ignore

        # End setup, start execution
        u.set_password("Tim")

        # End execution, start validation
        assert not u.check_password("mit")
        assert u.check_password("Tim")

    @pytest.mark.dependency(depends=["TestUser::test_password_hashing"])
    def test_required_form(self, client, testApp):
        """Integration Test registration form flow"""
        # Call register endpoint with some but not al form data
        response = client.post(
            "/auth/register", data={"username": "flask", "password": "tim"}
        )
        # Assert that the response is 200 and that the error message is in the response
        assert response.status_code == 200
        assert b"This field is required" in response.data

        # Since the form is not valid, assert that the user is not created in database
        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is None

        # Call register endpoint with ALL form data
        response = client.post(
            "/auth/register",
            data={
                "username": "flask",
                "password": "tim",
                "passwordRepeat": "tim",
                "email": "test@test.com",
            },
        )

        # Assert that the response is 302 and that the login page is in the response
        assert response.status_code == 302
        assert b"login" in response.data

        # Since the form is valid, assert that the user is created in database
        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is not None
