from models.user_response_model import UsersListResponse


class TestGetUsers:

    def test_get_users(self, users_client):
        page = 1
        response = users_client.get_users(page)

        users_client.check_response_and_status_code(response, 200, UsersListResponse)
        users_client.check_page_users(response, page)