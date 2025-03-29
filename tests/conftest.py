import os
import tempfile

import pytest
from flask.testing import FlaskClient

from flaskr import create_app
from flaskr.db import DB


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE_LOCATION': "test.sqlite",
    })
    yield app
    
@pytest.fixture
def db(app) -> DB:
    db = DB(app)
    with app.app_context():
        db.init_db()
        db.get_db().executescript(_data_sql)
    return db
    
@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
