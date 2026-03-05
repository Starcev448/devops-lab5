from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {"id": 1, "name": "Ivan Ivanov", "email": "i.i.ivanov@mail.com"},
    {"id": 2, "name": "Petr Petrov", "email": "p.p.petrov@mail.com"},
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={"email": users[0]["email"]})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={"email": "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user = {"name": "Diana Abulkdaifova", "email": "a.diana@gmail.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)  # вернулся id

    # Проверим, что реально создался
    response_get = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert response_get.status_code == 200
    data = response_get.json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]

def test_create_user_with_invalid_email():
    # email уже занят существующим пользователем
    existing_user = {"name": "Someone", "email": users[0]["email"]}
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    # создаём временного, чтобы удалить его (не трогаем дефолтных)
    temp_user = {"name": "Temp User", "email": "temp.user@mail.com"}
    create_resp = client.post("/api/v1/user", json=temp_user)
    assert create_resp.status_code == 201

    del_resp = client.delete("/api/v1/user", params={"email": temp_user["email"]})
    assert del_resp.status_code == 204

    # проверяем что удалился
    get_resp = client.get("/api/v1/user", params={"email": temp_user["email"]})
    assert get_resp.status_code == 404