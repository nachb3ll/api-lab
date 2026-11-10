import uuid

import pytest
import requests

SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    """Keep API requests on one server via the load-balancer cookie."""

    def request(self, method, url, *args, **kwargs):
        return super().request(method, SITE + url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    """Create a unique practice user and return its authorization header."""
    username = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": username, "password": "Pizza-2026"}

    created = api.post("/api/users", json=user)
    assert created.status_code == 201, created.text

    logged_in = api.post("/api/users/token/login", json=user)
    assert logged_in.status_code == 200, logged_in.text
    return {"Authorization": "token " + logged_in.json()["token"]}


@pytest.fixture
def auth(api):
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    response = api.post("/api/pizza", json={}, headers=auth)
    assert response.status_code == 200, response.text
    return response.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    """Create a test-owned rating and remove it after the test."""
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth
    )
    assert response.status_code == 201, response.text
    made = response.json()
    yield made
    deleted = api.delete(f"/api/ratings/{made['id']}", headers=auth)
    if deleted.status_code != 204:
        assert deleted.status_code == 400, deleted.text
        assert "not found" in deleted.json().get("error", "")


@pytest.fixture
def other_auth(api):
    return log_in_new_user(api)
