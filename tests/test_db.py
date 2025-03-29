import sqlite3
import random
import string
import pytest
from flask import g

class TestDB:
    def test_db_initialization(self, test_app, db):
        """Test that the DB class is properly initialized with the test_app."""
        assert hasattr(db, "_init_db_on_app"), "DB class should have init_db_on_test_app method"
        assert hasattr(db, "safe_query_execute"), "DB class should have safe_query_execute method"
        
        
    def test_safe_query_execute_not_found(self, test_app, db):
        """Test safe_query_execute returns 404 when no records are found."""
        with test_app.app_context():
            response, status_code = db.safe_query_execute("SELECT * FROM users WHERE id=999", {}, method="GET")
            assert status_code == 404
            assert response.json["message"] == "Execution successful, but haven't found anything"
            
    def test_safe_query_execute_sql_error(self, test_app, db):
        """Test safe_query_execute handles SQL errors properly."""
        with test_app.app_context():
            response, status_code = db.safe_query_execute("SELECT * FROM nonexistent_table", {}, method="GET")
            assert status_code == 500
            assert "error" in response.json

    def test_safe_query_execute_select(self, test_app, db):
        """Test safe_query_execute handles SQL errors properly."""
        with test_app.app_context():
            response, status_code = db.safe_query_execute("SELECT * FROM users WHERE id = 1", {}, method="GET")
            assert status_code == 200
            assert response.json["message"] == "Execution successful"
            assert len(response.json["data"])>0
        
    def test_safe_query_execute_insert(self, test_app, db):
        """Test safe_query_execute handles SQL errors properly."""
        with test_app.app_context():
            response, status_code = db.safe_query_execute(f"INSERT INTO users (username, password) VALUES ('{''.join(random.sample(string.digits, 8))}','pass')", {}, method="POST")
            assert status_code == 201
            assert response.json["message"] == "Execution successful"

    def test_db_closing(self, test_app, db):
        """Test that the database connection is properly closed after queries."""
        with test_app.app_context():
            db_conn = db.get_db()
            assert db_conn is not None, "Database should be open"
            db.close_db()
            assert "db" not in g, "Database should be closed after calling close_db()"