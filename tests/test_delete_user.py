import pytest
import allure
from assertions.base_assertions import Assertions


@allure.feature("User Management")
class TestDeleteUser:

    @allure.story("Delete existing user")
    @allure.title("Delete a created user and verify it's removed")
    def test_delete_user(self, users_client, prepare_user):
        # подготовка пользователя
        user_id = prepare_user

        with allure.step(f"Delete user id={user_id}"):
            response = users_client.delete_user(user_id)
            Assertions.assert_status_code(response, 204)

        with allure.step("Verify user is deleted and returns empty JSON"):
            users_client.check_deleted_user(user_id)

    @pytest.mark.xfail(reason="Reqres.in DELETE on nonexistent user may return 204 or 404", strict=False)
    @allure.story("Delete nonexistent user")
    @allure.title("Attempt to delete a nonexistent user id={user_id}")
    def test_negative_delete_user(self, users_client):
        with allure.step("Compute nonexistent user id"):
            user_id = users_client.get_nonexistent_user_id()

        with allure.step(f"Delete nonexistent user id={user_id}"):
            response = users_client.delete_user(user_id)

        with allure.step("Verify 404 status code for nonexistent deletion"):
            Assertions.assert_status_code(response, 404)
