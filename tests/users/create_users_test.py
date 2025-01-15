def test_create_user(client):
    payload = {
    "first_name": "Alex",
    "last_name": "Alexeev",
    "father_name" : "Ivanovich",
    "full_name": "Alex Ivanovich",
    "position" : "Worker",
    "phone" : "+3 (911) 181 00 32",
    "email" : "alex@mail.com",
    "telegram" : "@alex",
    "birthday" : "2001-02-02",
    "category" :"test user",
    "specialization" : "Working",
    "username" : "user_alex",
    "password"  : "123456789qqFF_",
    "notes" : "another test user",
    "role" : "user"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["first_name"] == "Alex"
    assert result["last_name"] == "Alexeev"
    assert result["father_name"] == "Ivanovich"
    assert result["position"] == "Worker"
    assert result["phone"] == "+3 (911) 181 00 32"
    assert result["email"] == "alex@mail.com"
    assert result["telegram"] == "@alex"
    assert result["birthday"] == "2001-02-02"
    assert result["category"] == "test user"
    assert result["specialization"] == "Working"
    assert result["username"] == "user_alex"
    assert result["password"] == "123456789qqFF_"
    assert result["notes"] == "another test user"
    assert result["role"] == "user"

def test_unauthenticated_user_cannot_create_user(client):
    client.headers = {}
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Ivanovich",
        "full_name": "Alex Ivanovich",
        "position": "Worker",
        "phone": "+3 (911) 181 00 32",
        "email": "alex@mail.com",
        "telegram": "@alex",
        "birthday": "2001-02-02",
        "category": "test user",
        "specialization": "Working",
        "username": "user_alex",
        "password": "123456789qqFF_",
        "notes": "another test user",
        "role": "user"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}

def test_cannot_create_user_with_empty_field(client):
    payload = {
        "first_name": "Alex"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 422

