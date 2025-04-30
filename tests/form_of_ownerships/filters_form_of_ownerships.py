def test_filters_customers(client, sample_form, another_form, third_form):

    response = client.get(
        "/form-of-ownership", params={"name": [sample_form.name, another_form.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_form.id,
            "name": sample_form.name,
        },
        {
            "id": another_form.id,
            "name": another_form.name,
        },
    ]
