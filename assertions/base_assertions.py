from json import JSONDecodeError
from typing import Any, Sequence
from requests import Response
from pydantic import ValidationError, BaseModel
from utils.logger import get_logger


logger = get_logger("Assertions")

class Assertions:
    @staticmethod
    def _parse_json(response: Response) -> Any:
        logger.debug(f"Parsing JSON from response text")
        try:
            return response.json()
        except JSONDecodeError:
            logger.error(
                f"Response is not in JSON format. Response text: {response.text}"
            )
            assert False, (
                "Response is not in JSON format. "
                f"Response text:\n{response.text}"
            )

    @staticmethod
    def assert_status_code(response: Response, expected: int) -> None:
        actual = response.status_code
        logger.info(f"Asserting status code: expected {expected}, actual {actual}")
        assert actual == expected, (
            f"Unexpected status code! Expected: {expected}. Actual: {actual}."
        )

    @staticmethod
    def assert_schema(response: Response, schema: type[BaseModel]):
        logger.info(f"Validating response schema against {schema.__name__}")
        try:
            # Pydantic v2
            schema.model_validate_json(response.text)
        except ValidationError as e:
            logger.error(f"Schema validation failed: {e}")
            raise AssertionError(f"Schema validation failed:\n{e}")

    @staticmethod
    def assert_json_has_key(response: Response, key: str) -> None:
        logger.info(f"Checking presence of key '{key}' in JSON")
        data = Assertions._parse_json(response)
        assert key in data, f"Response JSON doesn't have key '{key}'. Available: {list(data)}"

    @staticmethod
    def assert_json_has_keys(response: Response, *keys: str) -> None:
        logger.info(f"Checking presence of keys {keys} in JSON")
        data = Assertions._parse_json(response)
        missing = [k for k in keys if k not in data]
        assert not missing, f"Response JSON missing keys: {missing}. Available: {list(data)}"

    @staticmethod
    def assert_json_has_not_key(response: Response, key: str) -> None:
        logger.info(f"Ensuring key '{key}' is not in JSON")
        data = Assertions._parse_json(response)
        assert key not in data, f"Response JSON should not have key '{key}'"

    @staticmethod
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
            error_message or
            f"Value for '{key}' is wrong. Expected: {expected_value}, Actual: {actual}"
        )
