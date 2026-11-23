import unittest
from unittest.mock import patch

from app import create_app
from app.db import get_connection


class EmployeeApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    @patch("app.db.mysql.connect")
    def test_get_connection_uses_connector_module(self, connect):
        with self.app.app_context():
            get_connection()

        connect.assert_called_once_with(
            host=self.app.config["MYSQL_HOST"],
            port=self.app.config["MYSQL_PORT"],
            user=self.app.config["MYSQL_USER"],
            password=self.app.config["MYSQL_PASSWORD"],
            database=self.app.config["MYSQL_DATABASE"],
        )

    @patch("app.services.employee_service.employee_repository.get_all")
    def test_get_employees(self, get_all):
        get_all.return_value = [{"id": 1, "name": "Alex Morgan"}]

        response = self.client.get("/api/employees")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"id": 1, "name": "Alex Morgan"}])

    @patch("app.services.employee_service.employee_repository.get_by_id")
    def test_get_employee_by_id(self, get_by_id):
        get_by_id.return_value = {"id": 1, "name": "Alex Morgan"}

        response = self.client.get("/api/employees/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], 1)

    @patch("app.services.employee_service.employee_repository.get_by_id")
    @patch("app.services.employee_service.employee_repository.create")
    def test_post_employee(self, create, get_by_id):
        create.return_value = 1
        get_by_id.return_value = {"id": 1, "name": "Alex Morgan"}

        response = self.client.post(
            "/api/employees",
            json={
                "name": "Alex Morgan",
                "email": "alex@example.com",
                "department": "Engineering",
                "salary": 75000,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["id"], 1)

    def test_post_rejects_missing_fields(self):
        response = self.client.post("/api/employees", json={"name": "Alex"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required field", response.get_json()["error"])

    @patch("app.services.employee_service.employee_repository.get_by_id")
    @patch("app.services.employee_service.employee_repository.update")
    def test_patch_updates_only_supplied_fields(self, update, get_by_id):
        get_by_id.side_effect = [
            {"id": 1, "name": "Alex Morgan"},
            {"id": 1, "name": "Alex Morgan", "department": "Sales"},
        ]

        response = self.client.patch(
            "/api/employees/1",
            json={"department": "Sales"},
        )

        self.assertEqual(response.status_code, 200)
        update.assert_called_once_with(1, {"department": "Sales"})

    @patch("app.services.employee_service.employee_repository.get_by_id")
    @patch("app.services.employee_service.employee_repository.update")
    def test_put_replaces_employee(self, update, get_by_id):
        employee = {
            "id": 1,
            "name": "Alex Morgan",
            "email": "alex@example.com",
            "department": "Engineering",
            "salary": 75000,
        }
        get_by_id.side_effect = [employee, employee]

        response = self.client.put(
            "/api/employees/1",
            json={
                "name": "Alex Morgan",
                "email": "alex@example.com",
                "department": "Engineering",
                "salary": 75000,
            },
        )

        self.assertEqual(response.status_code, 200)
        update.assert_called_once_with(
            1,
            {
                "name": "Alex Morgan",
                "email": "alex@example.com",
                "department": "Engineering",
                "salary": 75000,
            },
        )

    @patch("app.services.employee_service.employee_repository.delete")
    def test_delete_employee(self, delete):
        delete.return_value = True

        response = self.client.delete("/api/employees/1")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")


if __name__ == "__main__":
    unittest.main()
