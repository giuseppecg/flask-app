import sqlite3

import pytest
from flaskr.db import get_db, safe_query_execute



def test_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
    
    
def test_safe_query_execute_success_201(monkeypatch, app):
    q = "INSERT INTO (username, password) VALUES (:username,:password);"
    def mock_get_db():
        class MockDB:
            def execute(self, query, params):
                return None
            def commit(self):
                pass 
        return MockDB()
    
    monkeypatch.setattr("app.get_db", mock_get_db)
    
    with app.app_context():
        response, status_code = safe_query_execute(q, params=dict(username="a_name", paswword="A_password", method="POST"))
        assert status_code = 201
        assert response["message"] = "Execution successful"
    