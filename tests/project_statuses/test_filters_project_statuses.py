def test_filters_project_statuses(
    client, sample_project_status, another_project_status, in_progress_status
):
    response = client.get(
        "/project-statuses",
        params={"name": [sample_project_status.name, another_project_status.name]},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_project_status.id,
            "name": sample_project_status.name,
        },
        {
            "id": another_project_status.id,
            "name": another_project_status.name,
        },
    ]
