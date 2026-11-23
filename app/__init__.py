import logging

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.errors import EmployeeNotFoundError, ValidationError
from app.routes.employee_routes import employee_blueprint
from app.routes.health_routes import health_blueprint
from app.db import mysql


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    app.register_blueprint(health_blueprint)
    app.register_blueprint(employee_blueprint, url_prefix="/api/employees")

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(EmployeeNotFoundError)
    def handle_employee_not_found(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(mysql.IntegrityError)
    def handle_integrity_error(error):
        return jsonify({"error": "An employee with that email already exists"}), 409

    @app.errorhandler(mysql.Error)
    def handle_database_error(error):
        app.logger.exception("Database request failed", exc_info=error)
        return jsonify({"error": "Database request failed"}), 503

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unexpected request failure")
        return jsonify({"error": "Internal server error"}), 500

    logging.basicConfig(level=logging.INFO)
    return app
