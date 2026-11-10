import requests

SITE = "https://quickpizza.grafana.com"


# The list of pizza names answers 200 and includes Margherita.
def test_names_are_listed():
    response = requests.get(SITE + "/api/names")
    assert response.status_code == 200
    assert "Margherita" in response.json()["names"]
