from client import client
from test_register import register


def login(client, username="", password=""):
    return client.post(
        "/api/login",
        json={"username": username, "password": password},
        follow_redirects=True,
    )


def test_login_fails_missing_json(client):
    resp = client.post("/api/login", follow_redirects=True,)
    assert resp.json.get("message") == "Missing JSON in request"


def test_login_fails_on_no_username(client):
    resp = login(client)
    assert resp.json.get("message") == "Username is required."


def test_login_fails_on_no_password(client):
    resp = login(client, "username")
    assert resp.json.get("message") == "Password is required."


def test_login_fails_user_not_found(client):
    resp = login(client, "username", "password")
    assert resp.json.get("message") == "User not found."


def test_login_fails_invalid_password(client):
    register(client, "username", "username@gmail.com", "password", "password")
    resp = login(client, "username", "notmypassword")
    assert resp.json.get("message") == "Invalid password."


def test_login_succeeds(client):
    register(client, "username", "username@gmail.com", "password", "password")
    resp = login(client, "username", "password")
    assert resp.json.get("message") == "Successfully logged in!"
