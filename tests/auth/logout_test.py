import pytest


@pytest.mark.skip(reason="TODO")
def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["refresh_token"] is not None
