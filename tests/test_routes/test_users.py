import json


def test_create_user(client):
    data = {
        "name": "name",
        "last_name": "lastname",
        "email": "testuser@nofoobar.com",
        "password": "Testing12",
    }
    response = client.post("/", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
