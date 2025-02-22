def test_delete_project_status(client, sample_project_status):
    response = client.delete(f"/project-statuses/{sample_project_status.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_project_status(
    client, sample_project_status
):
    client.headers = {}
    response = client.delete(f"/project-statuses/{sample_project_status.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
