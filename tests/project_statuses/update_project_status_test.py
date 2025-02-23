def test_update_project_status(client, sample_project_status):
    payload = {"name": "newtest object"}
    response = client.patch(
        f"/project-statuses/{sample_project_status.id}", json=payload
    )
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "newtest object"


def test_unauthenticated_user_cannot_update_project_status(
    client, sample_project_status
):
    client.headers = {}
    payload = {"name": "newtest object"}
    response = client.patch(
        f"/project-statuses/{sample_project_status.id}", json=payload
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
