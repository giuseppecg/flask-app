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
    username, password = request.args.get("username", "password")
    app.logger.debug(f"Registering {username} in db")
    cursor = db.get_db().cursor()
    create_new_user = f"INSERT INTO users VALUES ({username},{password});"
    try:
        cursor.execute(create_new_user)
    except Exception:
        app.logger.error(f"Could not register {username}")
    finally:
        db.close_db()


@app.put("/users/<int:id_user>")
def edit_user_by_id(id_user):
    raise NotImplementedError

@app.delete("/users/<int:id_user>")
def delete_user_by_id(id_user):
    raise NotImplementedError
