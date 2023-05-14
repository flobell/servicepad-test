from flask import url_for



def test_api_users_put(client, access_token):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.put(
        url_for("api.users"),
        json={
            "fullname": "Test Name Updated"
        },
        headers=headers
    )

    assert response.status_code == 200



def test_api_users_delete(client, access_token):
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' 
    }

    response = client.delete(url_for("api.users"), headers=headers)

    assert response.status_code == 200
