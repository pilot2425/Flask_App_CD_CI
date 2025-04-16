from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from app.models import Data
from app import db

data_routes = Blueprint("data_routes", __name__)


@data_routes.route("/data", methods=["POST"])
def insert_data():
    data = request.json
    new_data = Data(name=data.get("name"))

    current_data = Data.query.filter_by(name=data.get("name")).first()
    if current_data:
        return {"message": "Data already exists"}, 409

    db.session.add(new_data)
    db.session.commit()

    return jsonify({
        "message": "Data inserted successfully",
        "id": new_data.id,  # <- esto es lo que necesitas
        "name": new_data.name
    }), 201



@data_routes.route("/data", methods=["GET"])
def get_all_data():
    data_list = [{"id": data.id, "name": data.name} for data in Data.query.all()]
    return jsonify(data_list)


@data_routes.route("/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    session = db.session
    element_to_delete = session.get(Data, id)

    if not element_to_delete:
        return {"message": "Data not found"}, 404

    session.delete(element_to_delete)
    session.commit()
    return {"message": "Data deleted successfully"}

@data_routes.route("/tables", methods=["GET"])
def get_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify({"tables": tables})

@data_routes.route("/data/<int:id>", methods=["PUT"])
def update_data(id):
    data = request.json
    new_name = data.get("name")

    if not new_name:
        return {"message": "New name is required"}, 400

    element_to_update = db.session.get(Data, id)
    if not element_to_update:
        return {"message": "Data not found"}, 404

    element_to_update.name = new_name
    db.session.commit()

    return jsonify({
        "message": "Data updated successfully",
        "id": element_to_update.id,
        "name": element_to_update.name
    }), 200



