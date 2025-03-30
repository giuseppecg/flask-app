import os

from flask import Flask

from .db import DB


def create_app(test_config=None) -> tuple[Flask, DB]:
    """
    Create and configure the app. It creates the app instance and
    configures the database.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_LOCATION=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db = DB(app)

    return app, db
