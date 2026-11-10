import uuid


# A username that is already registered is rejected with a clear error.
def test_duplicate_username_is_refused(api):
    username = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": username, "password": "Pizza-2026"}
    first = api.post("/api/users", json=user)
    assert first.status_code == 201, first.text
    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json() == {"error": "username already taken"}


# Logging in with the wrong password is refused.
def test_wrong_password_is_refused(api):
    username = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": username, "password": "Pizza-2026"}
    created = api.post("/api/users", json=user)
    assert created.status_code == 201, created.text
    response = api.post(
        "/api/users/token/login",
        json={"username": username, "password": "Wrong-Password"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}


# An empty username is refused with a validation error.
def test_empty_username_is_refused(api):
    response = api.post(
        "/api/users", json={"username": "", "password": "Pizza-2026"}
    )
    assert response.status_code == 400
    assert response.json() == {"error": "username field is empty"}
