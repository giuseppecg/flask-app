import json

from flaskr import create_app


class TestMainRoutes:
    def test_config(self):
        """Test the default configuration."""
        assert not create_app()[0].testing
        assert create_app({"TESTING": True})[0].testing

    def test_hello(self, main_client):
        """Test the hello route."""
        response = main_client.get("/")
        assert response.data == b"This is Giuseppe's Flask app"

    def test_get_users(self, main_client):
        """Test the get_all_users route. It should return a list of users."""
        response = main_client.get("/users")
        assert len(json.loads(response.data)["data"]) > 0
        assert response.status_code == 200

    def test_get_user_by_id(self, main_client):
        """Test the get_users_by_id route. It should return a specific user."""
        response = main_client.get("/users/2")
        assert len(json.loads(response.data)["data"]) == 1
        assert response.status_code == 200

    def test_post_new_user(self, main_client):
        """Test the create_new_user route. It should create a new user."""
        response = main_client.post("/users?username=a_name&password=a_word")
        assert len(json.loads(response.data)["data"]) == 0
        assert response.status_code == 201

    def test_post_new_user_fail_one_param(self, main_client):
        """Test the create_new_user route. It should create a new user."""
        response = main_client.post("/users?username=a_name")
        assert json.loads(response.data)["message"] == "NOT NULL constraint failed: users.password"
        assert response.status_code == 500

    def test_edit_user_by_id(self, main_client):
        """
        Test the edit_user_by_id route. It should update a specific user
        with username and password as obligatory parameters.
        """
        response = main_client.put("/users/1?username=same&password=new_word")
        assert json.loads(response.data)["message"] == "Execution successful"
        assert response.status_code == 201

    def test_edit_user_fail_one_param(self, main_client):
        """
        Test the edit_user_by_id route. It should fail the update a specific user due to
        the lack of parameters.
        """
        response = main_client.put("/users/1?password=new_word")
        assert json.loads(response.data)["message"] == "NOT NULL constraint failed: users.username"
        assert response.status_code == 500

    def test_delete_user_by_id(self, main_client):
        """Test the delete_user_by_id route. It should delete a specific user."""
        response = main_client.delete("/users/1")
        assert json.loads(response.data)["message"] == "Execution successful"
        assert response.status_code == 201
