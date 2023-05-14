from flask import url_for


def test_api_publications_post(client, access_token):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.post(
        url_for("api.publications"),
        json={
            "title": "Test Publication",
            "description": "This is a test publication",
            "priority": 1,
            "status": "active"
        },
        headers=headers
    )

    assert response.status_code == 200


def test_api_publications_get(client, access_token):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.post(
        url_for("api.publications"),
        json={
            "title": "Test Publication",
            "description": "This is a test publication",
            "priority": 1,
            "status": "active",
            "user": "test@example.com",
        },
        headers=headers
    )

    assert response.status_code == 200


def test_api_publications_id_get(client, access_token, publication):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.get(url_for("api.publications_id", publication_id=publication.id), headers=headers)

    assert response.status_code == 200


def test_api_publications_id_put(client, access_token, publication):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.put(
        url_for("api.publications_id", publication_id=publication.id),
        json={
            "description": "This is an updated to publication",
            "priority": 2,
            "status": "inactive",
        },
        headers=headers
    )

    assert response.status_code == 200



def test_api_publications_id_delete(client, access_token, publication):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.delete(url_for("api.publications_id", publication_id=publication.id), headers=headers)

    assert response.status_code == 200
