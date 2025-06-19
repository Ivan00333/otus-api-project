from models.user_request_model import CreateUserRequest
from models.user_response_model import CreateUserResponse


class TestUserOperations:

    def test_create_user(self, users_client):
        response = users_client.create_user(CreateUserRequest)
        users_client.check_response_and_status_code(response, 201, CreateUserResponse)