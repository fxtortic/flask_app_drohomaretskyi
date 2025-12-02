import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest

from app import app, db
from app.users.models import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        User.query.delete()
        db.session.commit()

        with app.test_client() as client:
            yield client

        User.query.delete()
        db.session.commit()

def test_login_and_register_pages_load(client):
    resp = client.get("/users/login")
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert "Login" in text
    assert "Username" in text

    resp = client.get("/users/register")
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert "Register" in text
    assert "E-mail" in text

def test_register_creates_user_in_db(client):
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
        "confirm_password": "secret123",
        "submit": "Sign up",
    }

    resp = client.post(
        "/users/register",
        data=form_data,
        follow_redirects=True,
    )

    assert resp.status_code == 200

    text = resp.get_data(as_text=True)
    assert "Обліковий запис для testuser створено успішно!" in text

    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.email == "test@example.com"
        assert user.password_hash is not None
        assert user.password_hash != "secret123"


def _create_user(username: str, email: str, password: str) -> None:
    with app.app_context():
        user = User(username=username, email=email, password_hash="")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


def test_login_and_logout_flow(client):
    _create_user("loginuser", "login@example.com", "mypassword")

    resp = client.post(
        "/users/login",
        data={
            "username": "loginuser",
            "password": "mypassword",
            "remember": "y",
            "submit": "Login",
        },
        follow_redirects=True,
    )

    assert resp.status_code == 200
    text = resp.get_data(as_text=True)

    assert "Вхід виконано успішно." in text
    assert "Профіль" in text
    assert "Вітаю, loginuser" in text

    resp = client.get("/users/logout", follow_redirects=True)
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)

    assert "Ви вийшли із системи." in text
    assert "Login" in text
