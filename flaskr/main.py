from flaskr import create_app
from flaskr import users_view 


app, db = create_app()
app.extensions["db"] = db

app.add_url_rule("/", view_func=users_view.first_page, methods=["GET"])
app.add_url_rule("/users", view_func=users_view.get_all_users, methods=["GET"])
app.add_url_rule("/users/<int:id_user>", view_func=users_view.get_users_by_id, methods=["GET"])
app.add_url_rule("/users", view_func=users_view.create_new_user, methods=["POST"])
app.add_url_rule("/users/<int:id_user>", view_func=users_view.edit_user_by_id, methods=["PUT"])
app.add_url_rule("/users/<int:id_user>", view_func=users_view.delete_user_by_id, methods=["DELETE"])

def get_app():
    """
    Returns the app instance. To be used 
    """
    return app