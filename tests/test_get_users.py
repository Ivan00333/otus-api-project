from models.user_response_model import UsersListResponse
import allure
import pytest


@allure.feature("User Management")
class TestGetUsers:

    @allure.story("Get users list")
    @allure.title("Retrieve users list for page {page}")
    @pytest.mark.parametrize("page", [1, 2, 3])
    def test_get_users(self, users_client, page):
        with allure.step(f"Request users page={page}"):
            response = users_client.get_users(page)
        with allure.step(f"Verify status 200 and response schema UsersListResponse for page={page}"):
            users_client.check_response_and_status_code(response, 200, UsersListResponse)
        with allure.step(f"Verify returned page equals requested page={page}"):
            users_client.check_page_users(response, page)