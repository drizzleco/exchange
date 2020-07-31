from client import client


def logout(client):
    return client.delete("/api/logout",)


def test_logout_succeeds(client):
    resp = logout(client)
    assert resp.json.get("message") == "Successfully logged out"
