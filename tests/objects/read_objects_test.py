import pytest



async def test_get_objects(client):
    response = client.get("/objects")
    assert response.status_code == 200


# def test_unauthenticated_user_cannot_read_users(unauthorized_api_client):
#     response = unauthorized_api_client.get("/objects")
#     assert response.status_code == 401
#     assert response.json() == {'detail': 'Отсутствует токен'}