from app.db import get_connection
from app.db import mysql

EMPLOYEE_COLUMNS = ("name", "email", "department", "salary")


def get_all():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, department, salary, created_at, updated_at "
            "FROM employees ORDER BY id"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_by_id(employee_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, department, salary, created_at, updated_at "
            "FROM employees WHERE id = %s",
            (employee_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def create(employee_data):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO employees (name, email, department, salary) "
            "VALUES (%s, %s, %s, %s)",
            tuple(employee_data[column] for column in EMPLOYEE_COLUMNS),
        )
        employee_id = cursor.lastrowid
        connection.commit()
        return employee_id
    except mysql.Error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def update(employee_id, employee_data):
    assignments = ", ".join(f"{column} = %s" for column in employee_data)
    values = tuple(employee_data.values()) + (employee_id,)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"UPDATE employees SET {assignments} WHERE id = %s",
            values,
        )
        connection.commit()
    except mysql.Error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def delete(employee_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        deleted = cursor.rowcount > 0
        connection.commit()
        return deleted
    except mysql.Error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
