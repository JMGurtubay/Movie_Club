from typing import List


def test_create_user(client):
    response = client.post("/user", json={
        "username": "Jose",
        "password": "Pa$$w0rd",
        "email":"user@example.com"
    })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "El usuario ha sido creada exitosamente."
    assert json_response["description"] == "El usuario ha sido añadida correctamente a la base de datos."
    assert json_response["data"]["username"] == "Jose"



def test_get_users(client):
    response = client.get("/user")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Usuarios obtenidos con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la lista de usuarios."
    assert isinstance(json_response["data"], list)



def test_get_user_by_id(client):
    user_response = client.post("/user", json={
        "username": "Sandra",
        "password": "Pa$$w0rd",
        "email":"user123@example.com"
    })
    user_id = user_response.json()["data"]["id"]

    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Usuario obtenido con éxito."
    assert json_response["description"] == "Se obtuvo correctamente el usuario solicitado."
    assert json_response["data"]["id"] == user_id
    assert json_response["data"]["username"] == "Sandra"



def test_update_user(client):
    user_response = client.post("/user", json={
        "username": "Lisa",
        "password": "Pa$$w0rd",
        "email":"lisa@example.com"
    })
    user_id = user_response.json()["data"]["id"]

    update_response = client.put(f"/user/{user_id}", json={
        "username": "Mario",
        "password": "Pa$$w0rd",
        "email":"mario@example.com"
    })
    assert update_response.status_code == 200
    json_response = update_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "El usuario ha sido actualizado exitosamente."
    assert json_response["description"] == "Los datos de el usuario se han modificado correctamente."
    assert json_response["data"]["username"] == "Mario"


def test_delete_movie(client):
    user_response = client.post("/user", json={
        "username": "Berry",
        "password": "Pa$$w0rd",
        "email":"berry@example.com"
    })
    user_id = user_response.json()["data"]["id"]

    delete_response = client.delete(f"/user/{user_id}")
    assert delete_response.status_code == 200
    json_response = delete_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "El usuario ha sido eliminada exitosamente."
    assert json_response["description"] == "Se eliminó correctamente el usuario de la base de datos."
    assert json_response["data"] is None


