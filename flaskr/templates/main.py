from flask import Flask

app = Flask(__name__)

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
    raise NotImplementedError


@app.put("/users/<int:id_user>")
def edit_user_by_id(id_user):
    raise NotImplementedError

@app.delete("/users/<int:id_user>")
def delete_user_by_id(id_user):
    raise NotImplementedError
