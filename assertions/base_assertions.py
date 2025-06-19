import json
from json import JSONDecodeError
from typing import Any, Sequence
from requests import Response
from pydantic import ValidationError, BaseModel


class Assertions:
    @staticmethod
    def _parse_json(response: Response) -> Any:
        try:
            return response.json()
        except JSONDecodeError:
            assert False, (
                f"Response is not in JSON format. "
                f"Response text:\n{response.text}"
            )

    @staticmethod
    def assert_status_code(response: Response, expected: int) -> None:
        actual = response.status_code
        assert actual == expected, (
            f"Unexpected status code! "
            f"Expected: {expected}. Actual: {actual}."
        )

    @staticmethod
    def assert_schema(response: Response, schema: type[BaseModel]):
        try:
            schema.model_validate_json(response.text)
        except ValueError as e:
            raise AssertionError(f"Schema validation failed:\n{e}")

    @staticmethod
    def assert_json_has_key(response: Response, key: str) -> None:
        data = Assertions._parse_json(response)
        assert key in data, f"Response JSON doesn't have key '{key}'. Available: {list(data)}"

    @staticmethod
    def assert_json_has_keys(response: Response, *keys: str) -> None:
        data = Assertions._parse_json(response)
        missing = [k for k in keys if k not in data]
        assert not missing, f"Response JSON missing keys: {missing}. Available: {list(data)}"

    @staticmethod
    def assert_json_has_not_key(response: Response, key: str) -> None:
        data = Assertions._parse_json(response)
        assert key not in data, f"Response JSON should not have key '{key}'"

    @staticmethod
    def assert_json_value(
        response: Response,
        key: str,
        expected_value: Any,
        error_message: str = None
    ) -> None:

        data = Assertions._parse_json(response)
        assert key in data, f"Response JSON doesn't have key '{key}'"
        actual = data[key]
        assert actual == expected_value, (
            error_message or
            f"Value for '{key}' is wrong. Expected: {expected_value}, Actual: {actual}"
        )
