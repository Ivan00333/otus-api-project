from json import JSONDecodeError
from typing import Any
from requests import Response
from pydantic import ValidationError, BaseModel
from utils.logger import get_logger
import allure


logger = get_logger("Assertions")


class Assertions:

    @staticmethod
    @allure.step("Parse JSON response")
    def _parse_json(response: Response) -> Any:
        logger.debug("Parsing JSON from response")
        try:
            return response.json()
        except JSONDecodeError:
            logger.error(f"Response is not JSON. Text: {response.text}")
            assert False, (
                "Response is not in JSON format. "
                f"Response text:\n{response.text}"
            )

    @staticmethod
    @allure.step("Assert status code is {expected}")
    def assert_status_code(response: Response, expected: int) -> None:
        actual = response.status_code
        logger.info(f"Expected status {expected}, got {actual}")
        assert actual == expected, (
            f"Unexpected status code! Expected: {expected}. Actual: {actual}."
        )

    @staticmethod
    @allure.step("Validate response schema against")
    def assert_schema(response: Response, schema: type[BaseModel]):
        logger.info(f"Validating response schema against {schema.__name__}")
        try:
            schema.model_validate_json(response.text)
        except ValidationError as e:
            logger.error(f"Schema validation failed: {e}")
            raise AssertionError(f"Schema validation failed:\n{e}")

    @staticmethod
    @allure.step("Assert JSON has key '{key}'")
    def assert_json_has_key(response: Response, key: str) -> None:
        logger.info(f"Checking presence of key '{key}' in JSON")
        data = Assertions._parse_json(response)
        assert key in data, f"Response JSON doesn't have key '{key}'. Available: {list(data)}"

    @staticmethod
    @allure.step("Assert JSON has keys {keys}")
    def assert_json_has_keys(response: Response, *keys: str) -> None:
        logger.info(f"Checking presence of keys {keys} in JSON")
        data = Assertions._parse_json(response)
        missing = [k for k in keys if k not in data]
        assert not missing, f"Missing keys: {missing}. Available: {list(data)}"

    @staticmethod
    @allure.step("Assert JSON does not have key '{key}'")
    def assert_json_has_not_key(response: Response, key: str) -> None:
        logger.info(f"Ensuring key '{key}' is not in JSON")
        data = Assertions._parse_json(response)
        assert key not in data, f"Response JSON should not have key '{key}'"

    @staticmethod
    @allure.step("Assert JSON value for key '{key}' is '{expected_value}'")
    def assert_json_value(
        response: Response,
        key: str,
        expected_value: Any,
        error_message: str = None
    ) -> None:
        logger.info(f"Asserting JSON value for key '{key}' equals {expected_value}")
        data = Assertions._parse_json(response)
        assert key in data, f"Response JSON doesn't have key '{key}'"
        actual = data[key]
        assert actual == expected_value, (
            error_message or f"Key '{key}' value mismatch. Expected: {expected_value}, Actual: {actual}"
        )
