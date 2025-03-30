from flaskr import create_app
from flaskr import users_view


app, db = create_app()
app.extensions["db"] = db
app.url_map.strict_slashes = False
app.register_blueprint(users_view.bp_users, url_prefix="/users")


@app.route("/", methods=["GET"])
def first_page() -> str:
    """First page of the app. It returns a string."""
    return "This is Giuseppe's Flask app"


def get_app():
    """
    Returns the app instance. To be called by waitress
    """
    return app
