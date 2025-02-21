def test_delete_projects(client, sample_project):
    response = client.delete(f"/projects/{sample_project.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_projects(client, sample_project):
    client.headers = {}
    response = client.delete(f"/projects/{sample_project.id}")
    assert response.status_code == 401
