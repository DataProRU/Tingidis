def test_get_empty_deadlines(client):
    response = client.get("/deadlines")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_deadlines(client):
    client.headers = {}
    response = client.get("/deadlines")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_deadlines(
    client, sample_project, another_project, sample_agreement, another_agreement
):
    response = client.get("/deadlines")
    assert response.status_code == 200
    assert response.json() == [
        {
            "date": sample_agreement.deadline.isoformat(),
            "name": sample_agreement.name,
            "type": 1,
        },
        {
            "date": sample_project.deadline.isoformat(),
            "name": sample_project.name,
            "type": 3,
        },
        {
            "date": another_agreement.deadline.isoformat(),
            "name": another_agreement.name,
            "type": 1,
        },
        {
            "date": another_project.deadline.isoformat(),
            "name": another_project.name,
            "type": 3,
        },
    ]


def test_filtering_deadlines(
    client, sample_project, another_project, sample_agreement, another_agreement
):
    response = client.get("/deadlines?after_date=2024-02-02")
    assert response.status_code == 200
    assert response.json() == [
        {
            "date": another_agreement.deadline.isoformat(),
            "name": another_agreement.name,
            "type": 1,
        },
        {
            "date": another_project.deadline.isoformat(),
            "name": another_project.name,
            "type": 3,
        },
    ]

    response = client.get("/deadlines?before_date=2024-02-02")
    assert response.status_code == 200
    assert response.json() == [
        {
            "date": sample_agreement.deadline.isoformat(),
            "name": sample_agreement.name,
            "type": 1,
        },
        {
            "date": sample_project.deadline.isoformat(),
            "name": sample_project.name,
            "type": 3,
        },
        {
            "date": another_agreement.deadline.isoformat(),
            "name": another_agreement.name,
            "type": 1,
        },
    ]

    response = client.get("/deadlines?after_date=2024-01-02&before_date=2024-02-03")
    assert response.status_code == 200
    assert response.json() == [
        {
            "date": sample_project.deadline.isoformat(),
            "name": sample_project.name,
            "type": 3,
        },
        {
            "date": another_agreement.deadline.isoformat(),
            "name": another_agreement.name,
            "type": 1,
        },
    ]
