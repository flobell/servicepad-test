from flask import url_for

def test_api_files_id_get(client, file):
    response = client.get(url_for("api.files_id", file_id=file.id))

    assert response.status_code == 200