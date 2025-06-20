from assertions.base_assertions import Assertions
from models.user_response_model import SingleUserResponse


class TestGetSingleUser:

    def test_get_single_user(self, users_client, prepare_user):
        user_id = prepare_user
        response = users_client.get_single_user(user_id)

        users_client.check_response_and_status_code(response, 200, SingleUserResponse)

    def test_user_not_found(self, users_client):
        bad_user_id = users_client.get_nonexistent_user_id()
        response = users_client.get_single_user(bad_user_id)

        Assertions.assert_status_code(response, 404)



