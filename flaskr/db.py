import sqlite3
from datetime import datetime

import click
from flask import current_app, g, jsonify


def get_db() -> g:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_LOCATION'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db() -> None:
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def close_db(e=None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_db_on_app(app):
    """"Method to be called inside the __init__ factory to start from scratch the db for each application"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(restart_db_command)

def safe_query_execute(query, method)->tuple:
    cursor = get_db().cursor()
    try:
        data = cursor.execute(query).fetchall()
    except sqlite3.Error as e:
        return jsonify({"message": str(e), "error": str(e)}), 500
    finally:
        close_db()
    
    if method == "POST":
        return jsonify({"message":"Execution successful", "data":data}), 201
    else:
        return jsonify({"message":"Execution successful", "data":data}), 200

@click.command('init-db')
def restart_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')