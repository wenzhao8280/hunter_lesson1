import os

from dotenv import load_dotenv

# Load variables from a .env file (if present) into the environment.
load_dotenv()


class Config:
    """Central place for app configuration.

    Reads everything from environment variables so secrets never live
    in the code. See .env.example for the variables this expects.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://casenext:casenext_dev_pw@localhost:5432/casenext_dev",
    )
    # We don't need SQLAlchemy's change-tracking events; turning this off
    # avoids extra memory use and a startup warning.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
