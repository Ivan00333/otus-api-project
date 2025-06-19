import pytest
from config import Settings
from api.users_client import get_users_client, UsersClient


@pytest.fixture(scope='session')
def settings():

    return Settings()

@pytest.fixture
def users_client(settings):

    return get_users_client(settings)


@pytest.fixture
def prepare_user(users_client):
    response = users_client.create_user()
    user_id = users_client.get_value_by_parameter(response, "id")

    yield user_id

    users_client.delete_user(user_id)