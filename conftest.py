import pytest
from config import Settings
from api.users_client import get_users_client, UsersClient


@pytest.fixture(scope='session')
def settings():

    return Settings()

@pytest.fixture
def users_client(settings):

    return get_users_client(settings)
