# The owner can still read their rating after another user tries to access it.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.get(path, headers=other_auth)
    assert 400 <= response.status_code <= 499

    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# The owner can still read the unchanged rating after another user tries to update it.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.put(path, json={"stars": 1}, headers=other_auth)
    assert 400 <= response.status_code <= 499

    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# The owner can still read the rating after another user tries to delete it.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.delete(path, headers=other_auth)
    assert 400 <= response.status_code <= 499

    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating
