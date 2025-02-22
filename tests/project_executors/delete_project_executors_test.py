def test_delete_project_executor(client, sample_project_executor):
    response = client.delete(f"/project-executors/{sample_project_executor.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_project_executor(
    client, another_project_executor
):
    client.headers = {}
    response = client.delete(f"/project-executors/{another_project_executor.id}")
    assert response.status_code == 401
