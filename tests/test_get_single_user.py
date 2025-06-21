from assertions.base_assertions import Assertions
from models.user_response_model import SingleUserResponse
import allure


@allure.feature("User Management")
class TestGetSingleUser:

    @allure.story("Get existing user")
    @allure.title("Retrieve a single user by id")
    def test_get_single_user(self, users_client, prepare_user):
        with allure.step("Get user id={prepare_user}"):
            response = users_client.get_single_user(prepare_user)
        with allure.step("Verify 200 status and schema SingleUserResponse"):
            users_client.check_response_and_status_code(response, 200, SingleUserResponse)

    @allure.story("Get nonexistent user")
    @allure.title("Attempt to retrieve a nonexistent user and expect 404")
    def test_user_not_found(self, users_client):
        with allure.step("Compute nonexistent user id"):
            bad_user_id = users_client.get_nonexistent_user_id()
        with allure.step(f"Get user id={bad_user_id}"):
            response = users_client.get_single_user(bad_user_id)
        with allure.step("Verify 404 status code for nonexistent user"):
            Assertions.assert_status_code(response, 404)



