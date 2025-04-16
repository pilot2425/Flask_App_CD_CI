import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app("development")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 404  # según tu ruta raíz


def test_add_data(client):
    response = client.post("/data", json={"name": "Test User"})
    assert response.status_code == 201


def test_get_data(client):
    # primero insertamos un registro
    client.post("/data", json={"name": "Test Get"})
    response = client.get("/data")
    assert response.status_code == 200
    assert b"Test Get" in response.data


def test_delete_data(client):
    # Crear primero un objeto
    post_response = client.post("/data", json={"name": "Test Delete"})
    assert post_response.status_code == 201
    response_json = post_response.get_json()
    data_id = response_json["id"]  # Al crear devolvemos el ID

    # Borrar ese objeto
    delete_response = client.delete(f"/data/{data_id}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Data deleted successfully"

    # Intentar borrarlo otra vez para comprobar el 404
    second_delete = client.delete(f"/data/{data_id}")
    assert second_delete.status_code == 404


def test_get_tables(client):
    response = client.get("/tables")
    assert response.status_code == 200

    data = response.get_json()
    assert "tables" in data
    table_exists = "data" in data["tables"]
    assert table_exists  # la tabla debe existir porque es la de prueba


def test_update_data(client):
    # Crear un registro primero
    post_resp = client.post("/data", json={"name": "Old Name"})
    assert post_resp.status_code == 201
    data_id = post_resp.get_json()["id"]

    # Actualizarlo
    put_resp = client.put(f"/data/{data_id}", json={"name": "New Name"})
    assert put_resp.status_code == 200
    json_data = put_resp.get_json()
    assert json_data["message"] == "Data updated successfully"
    assert json_data["name"] == "New Name"

    # Verificar que el cambio se refleja
    get_resp = client.get("/data")
    assert any(entry["name"] == "New Name" for entry in get_resp.get_json())


def test_update_nonexistent_data(client):
    # Intentar actualizar un ID que no existe
    response = client.put("/data/9999", json={"name": "Does Not Exist"})
    assert response.status_code == 404
    assert response.get_json()["message"] == "Data not found"


def test_update_data_without_name(client):
    # Crear un registro
    post_resp = client.post("/data", json={"name": "Incomplete"})
    data_id = post_resp.get_json()["id"]

    # Intentar actualizar sin enviar "name"
    response = client.put(f"/data/{data_id}", json={})
    assert response.status_code == 400
    assert response.get_json()["message"] == "New name is required"
    