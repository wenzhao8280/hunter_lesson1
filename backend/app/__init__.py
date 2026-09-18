from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    """Application factory: builds and configures the Flask app.

    Using a factory (instead of a single global `app`) keeps things
    testable and avoids import-order headaches with the database.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Allow the React dev server (different port) to call this API.
    CORS(app)

    # Import models so SQLAlchemy/Flask-Migrate know about every table.
    with app.app_context():
        from app import models  # noqa: F401

    from app.routes import register_routes

    register_routes(app)

    @app.route("/api/health")
    def health_check():
        return {"status": "ok"}

    return app
