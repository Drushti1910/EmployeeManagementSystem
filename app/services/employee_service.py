import math
import re
from collections.abc import Mapping

from app.errors import EmployeeNotFoundError, ValidationError
from app.repositories import employee_repository

REQUIRED_FIELDS = {"name", "email", "department", "salary"}
ALLOWED_FIELDS = REQUIRED_FIELDS
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_SALARY = 9_999_999_999.99


def get_employees():
    return employee_repository.get_all()


def get_employee(employee_id):
    employee = employee_repository.get_by_id(employee_id)
    if employee is None:
        raise EmployeeNotFoundError(f"Employee {employee_id} was not found")
    return employee


def create_employee(data):
    employee_data = _validate_employee_data(data, partial=False)
    employee_id = employee_repository.create(employee_data)
    return get_employee(employee_id)


def replace_employee(employee_id, data):
    get_employee(employee_id)
    employee_data = _validate_employee_data(data, partial=False)
    employee_repository.update(employee_id, employee_data)
    return get_employee(employee_id)


def update_employee(employee_id, data):
    get_employee(employee_id)
    employee_data = _validate_employee_data(data, partial=True)
    if not employee_data:
        raise ValidationError("Provide at least one employee field to update")
    employee_repository.update(employee_id, employee_data)
    return get_employee(employee_id)


def delete_employee(employee_id):
    if not employee_repository.delete(employee_id):
        raise EmployeeNotFoundError(f"Employee {employee_id} was not found")


def _validate_employee_data(data, partial):
    if not isinstance(data, Mapping):
        raise ValidationError("Request body must be a JSON object")

    unknown_fields = set(data) - ALLOWED_FIELDS
    if unknown_fields:
        names = ", ".join(sorted(unknown_fields))
        raise ValidationError(f"Unknown field(s): {names}")

    if not partial:
        missing_fields = REQUIRED_FIELDS - set(data)
        if missing_fields:
            names = ", ".join(sorted(missing_fields))
            raise ValidationError(f"Missing required field(s): {names}")

    validated = {}
    for field, value in data.items():
        if field in {"name", "email", "department"}:
            if not isinstance(value, str) or not value.strip():
                raise ValidationError(f"{field} must be a non-empty string")
            value = value.strip()
            if field == "email" and not EMAIL_PATTERN.fullmatch(value):
                raise ValidationError("email must be a valid email address")
        elif field == "salary":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError("salary must be a non-negative number")
            if value < 0 or value > MAX_SALARY or not math.isfinite(value):
                raise ValidationError(
                    f"salary must be between 0 and {MAX_SALARY}"
                )
        validated[field] = value

    return validated
