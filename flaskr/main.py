from flask import request, jsonify

from . import create_app,db

app = create_app()

@app.get("/")
def first_page():
    return "This is Giuseppe's Flask app"

@app.get("/users")
def get_all_users():
    get_users_query = "SELECT * FROM users" 
    return db.safe_query_execute(get_users_query,{}, method="GET")
    

@app.get("/users/<int:id_user>")
def get_users_by_id(id_user):
    get_user_by_id_query = "SELECT * FROM users WHERE id=:id_user"
    return db.safe_query_execute(get_user_by_id_query, params=dict(id_user=id_user), method="GET")

@app.post("/users")
def create_new_user():
    query_params = dict(username = request.args.get("username"), password = request.args.get("password"))
    app.logger.debug(f"Registering user {request.args.get("username")} in db")
    create_new_user_query = "INSERT INTO users (username, password) VALUES (:username,:password);"
    return db.safe_query_execute(create_new_user_query, params=query_params, method="POST")

@app.put("/users/<int:id_user>")
def edit_user_by_id(id_user):
    query_params = dict(username = request.args.get("username"), 
                        password = request.args.get("password"),
                        id_user = id_user)
    app.logger.debug(f"Editing user id {id_user} to {request.args.get("username")} in db")
    edit_user_by_id = "UPDATE users SET username=:username, password=:password WHERE id=:id_user"
    return db.safe_query_execute(edit_user_by_id, params=query_params, method="PUT")

@app.delete("/users/<int:id_user>")
def delete_user_by_id(id_user):
    delete_user_by_id = f"DELETE FROM users WHERE id={id_user}"
    app.logger.debug(f"Deleting user id {id_user} in db")
    return db.safe_query_execute(delete_user_by_id, params=dict(id_user=id_user), method="DELETE")
