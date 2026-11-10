# A newly created rating is returned with its id, stars and pizza.
def test_create_rating(api, auth, pizza_id):
    response = api.post(
        "/api/ratings", json={"pizza_id": pizza_id, "stars": 5}, headers=auth
    )
    assert response.status_code == 201
    body = response.json()
    assert body["stars"] == 5
    assert body["pizza_id"] == pizza_id
    assert isinstance(body["id"], int)


# A saved rating can be read back by its id.
def test_read_rating(api, auth, rating):
    response = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert response.status_code == 200
    assert response.json() == rating


# Changing the stars of a rating returns the updated value.
def test_update_rating(api, auth, rating):
    response = api.put(
        f"/api/ratings/{rating['id']}", json={"stars": 4}, headers=auth
    )
    assert response.status_code == 200
    assert response.json()["stars"] == 4


# A deleted rating can no longer be read.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.delete(path, headers=auth)
    assert response.status_code == 204
    response = api.get(path, headers=auth)
    assert response.status_code == 404
