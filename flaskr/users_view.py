from functools import wraps

from flask import Blueprint, request, jsonify, current_app

from flaskr.db import DB


def with_db(func):
    """Decorator to inject the DB instance into the route function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        db = current_app.extensions["db"]  # Retrieve the DB instance
        return func(db, *args, **kwargs)  # Pass it as the first argument

    return wrapper

bp_users = Blueprint("users", __name__)


@bp_users.route("/", methods=["GET"])
@with_db
def get_all_users(db: DB) -> tuple:
    """Get all users from the database. It returns a list of users."""
    get_users_query = "SELECT * FROM users"
    return db.safe_query_execute(get_users_query, {}, method="GET")


@bp_users.route("/<int:id_user>", methods=["GET"])
@with_db
def get_users_by_id(db: DB, id_user: int) -> tuple:
    """Get a specific user from the database. It returns a specific user."""
    get_user_by_id_query = "SELECT * FROM users WHERE id=:id_user"
    return db.safe_query_execute(get_user_by_id_query, params=dict(id_user=id_user), method="GET")


@bp_users.route("/", methods=["POST"])
@with_db
def create_new_user(db: DB) -> tuple:
    """Create a new user in the database. It informs the created user."""
    query_params = dict(
        username=request.args.get("username"), password=request.args.get("password")
    )
    current_app.logger.debug(f"Registering user {request.args.get("username")} in db")
    create_new_user_query = "INSERT INTO users (username, password) VALUES (:username,:password);"
    return db.safe_query_execute(create_new_user_query, params=query_params, method="POST")


@bp_users.route("/<int:id_user>", methods=["PUT"])
@with_db
def edit_user_by_id(db: DB, id_user: int) -> tuple:
    """Edit a specific user in the database. It returns the edited user."""
    query_params = dict(
        username=request.args.get("username"),
        password=request.args.get("password"),
        id_user=id_user,
    )
    current_app.logger.debug(f"Editing user id {id_user} to {request.args.get("username")} in db")
    edit_user_by_id = "UPDATE users SET username=:username, password=:password WHERE id=:id_user"
    return db.safe_query_execute(edit_user_by_id, params=query_params, method="PUT")


@bp_users.route("/<int:id_user>", methods=["DELETE"])
@with_db
def delete_user_by_id(db: DB, id_user: int) -> tuple:
    """Delete a specific user from the database. It returns the deleted user."""
    delete_user_by_id = f"DELETE FROM users WHERE id={id_user}"
    current_app.logger.debug(f"Deleting user id {id_user} in db")
    return db.safe_query_execute(delete_user_by_id, params=dict(id_user=id_user), method="DELETE")
