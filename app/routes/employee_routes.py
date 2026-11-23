from flask import Blueprint, jsonify, request

from app.services.employee_service import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    replace_employee,
    update_employee,
)

employee_blueprint = Blueprint("employees", __name__)


@employee_blueprint.get("")
def list_employees():
    return jsonify(get_employees())


@employee_blueprint.get("/<int:employee_id>")
def retrieve_employee(employee_id):
    return jsonify(get_employee(employee_id))


@employee_blueprint.post("")
def add_employee():
    employee = create_employee(request.get_json())
    return jsonify(employee), 201


@employee_blueprint.put("/<int:employee_id>")
def put_employee(employee_id):
    employee = replace_employee(employee_id, request.get_json())
    return jsonify(employee)


@employee_blueprint.patch("/<int:employee_id>")
def patch_employee(employee_id):
    employee = update_employee(employee_id, request.get_json())
    return jsonify(employee)


@employee_blueprint.delete("/<int:employee_id>")
def remove_employee(employee_id):
    delete_employee(employee_id)
    return "", 204
