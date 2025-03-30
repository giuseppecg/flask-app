import os
import tempfile

import pytest
from flask.testing import FlaskClient

from flaskr import create_app
from flaskr.db import DB
from flaskr.main import app


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def test_app():
    """Create a new app for testing"""
    test_app,_ = create_app(
        {
            "TESTING": True,
            "DATABASE_LOCATION": "test.sqlite",
        }
    )
    yield test_app


@pytest.fixture
def db(test_app) -> DB:
    """
    Initiates the DB for tests with the same schema as production. It uses the fixture
    that creates a new app.
    """
    db = DB(test_app)
    with test_app.app_context():
        db.init_db()
        db.get_db().executescript(_data_sql)
    return db


@pytest.fixture(scope="session")
def main_app():
    """
    Creates the app with the routes in main. It updates some configurations and
    start a db for testing.
    """
    app.config.update(
        {
            "TESTING": True,
            "DATABASE_LOCATION": "test_main.sqlite",
            "instance_relative_config": True,
        }
    )

    db = DB(app)
    with app.app_context():
        db.init_db()
        db.get_db().executescript(_data_sql)

    yield app


@pytest.fixture
def main_client(main_app) -> FlaskClient:
    """Starts a client for testing. This should be called in the test files for main routes"""
    return main_app.test_client()
