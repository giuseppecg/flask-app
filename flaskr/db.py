import json
import sqlite3
from datetime import datetime

import click
from flask import current_app, g, jsonify

class DB():
    
    def __init__(self, app=None):
        if app is not None:
            self.init_db_on_app(app)
    
    def init_db_on_app(self, app):
        """"Method to be called inside the __init__ factory to start from scratch the db for each application"""
        app.teardown_appcontext(self.close_db)
        app.cli.add_command(self.restart_db_command)
        
    def get_db(self) -> g:
        """Returns an instance of db so you can create a cursor and comunicate with it."""
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE_LOCATION'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db

    def init_db(self) -> None:
        """Starts th sqlite instance."""
        db = get_db()

        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

    def close_db(self, e=None) -> None:
        """Closes db instance. Should be called everytime the communication with the database is finished."""
        db = g.pop('db', None)

        if db is not None:
            db.close()
    
    @click.command('init-db')
    def restart_db_command(self) -> None:
        """Clear the existing data and create new tables."""
        self._init_app(app)
        click.echo('Initialized the database.')
        

    def safe_query_execute(self, query:str, params:dict, method:str="GET")->tuple:
        """"This method executes cleanly queries, handling errors and returning more precise codes and messages"""
        db = self.get_db()
        try:
            cur = db.execute(query, params)
            data = cur.fetchall() if method == "GET" else db.commit()
        except sqlite3.Error as e:
            return jsonify({"message": str(e), "error": str(e)}), 500
        finally:
            self.close_db()
        
        if method == "GET":
            if len(data)>0:
                return jsonify({"message":"Execution successful", "data":[dict(x) for x in data]}), 200
            else: 
                return jsonify({"message":"Execution successful, but haven't found anything", "data":""}), 404
        else:
            return jsonify({"message":"Execution successful", "data":""}), 201
