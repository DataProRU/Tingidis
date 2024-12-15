from fastapi.testclient import TestClient
from main import app  # Укажите ваш корневой модуль

client = TestClient(app)


def test_login():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 401  # Пример обработки невалидного логина
