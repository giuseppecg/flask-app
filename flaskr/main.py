from flask import request, jsonify

from . import create_app,db

app = create_app()

@app.get("/")
def first_page():
    return "This is Giuseppe's Flask app"

@app.get("/users")
def get_all_users():
    get_users_query = "SELECT * FROM users" 
    return db.safe_query_execute(get_users_query, "GET")
    

@app.get("/users/<int:id_user>")
def get_users_by_id(id_user):
    get_user_by_id_query = f"SELECT * FROM users WHERE id={id_user}"
    return db.safe_query_execute(get_user_by_id_query, "GET")

@app.post("/users")
def create_new_user():
    username, password = request.args.get("username"),request.args.get("password")
    app.logger.debug(f"Registering user {username} in db")
    create_new_user_query = f"INSERT INTO users (username, password) VALUES ('{username}','{password}');"
    return db.safe_query_execute(create_new_user_query, "POST")

@app.put("/users/<int:id_user>")
def edit_user_by_id(id_user):
    raise NotImplementedError

@app.delete("/users/<int:id_user>")
def delete_user_by_id(id_user):
    raise NotImplementedError
