import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
DECIMAL_ERROR = "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
TEXT_ERROR = "json: cannot unmarshal string into Go struct field Rating.stars of type int"


# Base choice: save 3 whole stars for an existing pizza using the user's own token.
def test_base_choice_is_saved(api, auth, pizza_id):
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth
    )
    assert response.status_code == 201
    assert response.json()["stars"] == 3
    assert response.json()["pizza_id"] == pizza_id


# Stars below 1 or above 5 are refused with the documented validation error.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth
    )
    assert response.status_code == 400
    assert response.json() == {"error": STARS_ERROR}


# A decimal stars value is refused because the API requires a whole number.
def test_decimal_stars_are_refused(api, auth, pizza_id):
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": 3.5}, headers=auth
    )
    assert response.status_code == 400
    assert response.json() == {"error": DECIMAL_ERROR}


# A text stars value is refused because the API requires a whole number.
def test_text_stars_are_refused(api, auth, pizza_id):
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": "3"}, headers=auth
    )
    assert response.status_code == 400
    assert response.json() == {"error": TEXT_ERROR}


# A missing stars field is refused with the range validation message.
def test_missing_stars_are_refused(api, auth, pizza_id):
    response = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert response.status_code == 400
    assert response.json() == {"error": STARS_ERROR}


# A rating for a pizza that does not exist is refused.
def test_unknown_pizza_is_refused(api, auth):
    response = api.post(
        "/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth
    )
    assert response.status_code == 400
    assert response.json() == {"error": "pizza ID 999999999 not found"}


# Creating a rating without an authorization token is refused.
def test_rating_without_token_is_refused(api, pizza_id):
    response = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}


# Creating a rating with a malformed token is refused.
def test_rating_with_wrong_token_is_refused(api, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers={"Authorization": "token short"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}
