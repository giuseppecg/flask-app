from flask import request, jsonify

from . import create_app,db

app = create_app()

@app.get("/")
def first_page():
    return "This is Giuseppe's Flask app"

@app.get("/users")
def get_all_users():
    raise NotImplementedError

@app.get("/users/<int:id_user>")
def get_users_by_id(id_user):
    raise NotImplementedError

@app.post("/users")
def create_new_user():
    username, password = request.args.get("username"),request.args.get("password")
    app.logger.debug(f"Registering user {username} in db")
    cursor = db.get_db().cursor()
    create_new_user = f"INSERT INTO users (username, password) VALUES ('{username}','{password}');"
    try:
        cursor.execute(create_new_user)
    except Exception as e:
        app.logger.error(f"Could not register user {username}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close_db()
    
    return jsonify({"message": "User added successfully!"}), 201


@app.put("/users/<int:id_user>")
def edit_user_by_id(id_user):
    raise NotImplementedError

@app.delete("/users/<int:id_user>")
def delete_user_by_id(id_user):
    raise NotImplementedError
