import pytest
from models.user_request_model import UpdateUserRequest
from models.user_response_model import UpdateUserResponse
from assertions.base_assertions import Assertions
import allure


@allure.feature("User Management")
class TestUpdateUser:

    @allure.story("Update existing user")
    @allure.title("Update a user's name and job successfully")
    def test_update_user(self, prepare_user, users_client):
        user_id = prepare_user
        new_name = 'Ivan'
        new_job = 'QA'

        with allure.step(f"Prepare payload for user id={user_id}"):
            payload = UpdateUserRequest(name=new_name, job=new_job)
        with allure.step(f"Send update request for user id={user_id}"):
            response = users_client.update_user(user_id, payload)
        with allure.step("Verify status 200 and response schema"):
            users_client.check_response_and_status_code(response, 200, UpdateUserResponse)
        with allure.step("Assert returned values are updated"):
            Assertions.assert_json_value(response, "name", new_name, "Name was not updated")
            Assertions.assert_json_value(response, "job",  new_job,   "Job was not updated")

    @pytest.mark.xfail(reason="Reqres.in does not validate empty or None fields", strict=False)
    @pytest.mark.parametrize(
        "new_name, new_job",
        [
            ("", ""),
            (None, None)
        ]
    )
    @allure.story("Update user with invalid data")
    @allure.title("Attempt to update user id={prepare_user} with invalid fields: name={new_name}, job={new_job}")
    def test_negative_update_user(self, prepare_user, users_client, new_name, new_job):
        user_id = prepare_user
        with allure.step(f"Construct invalid payload name={new_name}, job={new_job}"):
            payload = UpdateUserRequest(name=new_name, job=new_job)
        with allure.step(f"Send update request for user id={user_id}"):
            response = users_client.update_user(user_id, payload)
        with allure.step("Verify 400 status for invalid update"):
            users_client.check_response_and_status_code(response, 400, UpdateUserResponse)

    @pytest.mark.xfail(reason="Updating nonexistent user should return 404", strict=False)
    @allure.story("Update nonexistent user")
    @allure.title("Attempt to update a nonexistent user and expect 404")
    def test_update_user_wrong_id(self, users_client):
        with allure.step("Compute nonexistent user id"):
            user_id = users_client.get_nonexistent_user_id()
        with allure.step(f"Send update request for nonexistent user id={user_id}"):
            payload = UpdateUserRequest()
            response = users_client.update_user(user_id, payload)
        with allure.step("Verify 404 status for nonexistent user update"):
            Assertions.assert_status_code(response, 404)
