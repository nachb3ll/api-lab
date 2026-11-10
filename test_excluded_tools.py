import pytest


# A pizza does not use any tool that the customer excluded.
@pytest.mark.parametrize("excluded", [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]])
def test_excluded_tools_are_not_used(api, auth, excluded):
    response = api.post(
        "/api/pizza", json={"excludedTools": excluded}, headers=auth
    )
    assert response.status_code == 200
    assert response.json()["pizza"]["tool"] not in excluded


# Excluding every available tool should return a client error with a JSON explanation.
@pytest.mark.xfail(
    reason="Defect 1: excluding all tools returns 500 with an empty body instead of a 400 JSON error",
    strict=True,
)
def test_excluding_all_tools_returns_client_error(api, auth):
    response = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert response.json().get("error")

