import pytest


# Updating a rating accepts only its boundary values from 1 through 5.
@pytest.mark.parametrize(
    ("stars", "expected_status"), [(0, 400), (1, 200), (5, 200), (6, 400)]
)
def test_update_rating_boundary_values(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    response = api.put(path, json={"stars": stars}, headers=auth)
    assert response.status_code == expected_status

    reread = api.get(path, headers=auth)
    assert reread.status_code == 200
    expected_stars = stars if expected_status == 200 else 3
    assert reread.json()["stars"] == expected_stars
