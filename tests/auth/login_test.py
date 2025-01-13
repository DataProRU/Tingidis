def test_login_user(client):
    pass
    # client.headers = {}
    # payload = {
    #     "username": "user",
    #     "password": "123456789",
    # }
    # response = client.post("/login", json=payload)
    # assert response.status_code == 200


def test_login_with_incorrect_data(client):
    client.headers = {}
    payload = {
        "username": "user",
        "password": "1234567810",
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Неверный логин или пароль'}


def test_login_with_empty_field(client):
    client.headers = {}
    payload = {
        "username": "user"
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 422