"""Shared extension instances.

These are created here (not inside app/__init__.py) so model files can
do `from app.extensions import db` without triggering a circular import
with the app factory.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
