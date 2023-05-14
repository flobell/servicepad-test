from flask import url_for

def test_api_auth_signup(client):
    response = client.post(
        url_for("api.auth_signup"),
        json={
            "email": "test@example.com",
            "password": "password",
            "fullname": "Test User",
        },
    )
    assert response.status_code == 200


def test_api_auth_login(client):
    client.post(
        url_for("api.auth_signup"),
        json={
            "email": "test@example.com",
            "password": "password",
            "fullname": "Test User",
        },
    )

    response = client.post(
        url_for("api.auth_login"),
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json

def test_api_auth_logout(client, access_token):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.post(url_for("api.auth_logout"),headers=headers)

    assert response.status_code == 200
