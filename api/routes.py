from enum import Enum


class ApiRoutes(Enum):
    GET_USERS = "users?page={page}"
    GET_SINGLE_USER = "users/{id}"
    CREATE_USER = "users"
    UPDATE_USER = "users/{id}"
    DELETE_USER = "users/{id}"
    REGISTER = "register"
    LOGIN = "login"
    DELAYED_RESPONSE = "users?delay={seconds}"

    def __str__(self):
        return self.value

    def with_id(self, **kwargs):
        return self.value.format(**kwargs)
