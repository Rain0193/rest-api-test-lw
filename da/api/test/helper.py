import requests
from jsonpath_rw import parse


class Json(object):
    """Provide json-related functions"""
    @staticmethod
    def get_values_from_json(json_object, json_path):
        """Get values from json_object with the given json path"""
        return [match.value for match in parse(json_path).find(json_object)] if json_object and json_path else []

    @staticmethod
    def get_value_from_json(json_object, json_path):
        """Get a value from json_object with the given json path"""
        results = Json.get_values_from_json(json_object, json_path)
        return next(iter(results or []), None)


class API(object):
    """Provide API-related functions"""
    @staticmethod
    def get_status_code(uri, params, timeout):
        """Get the HTTP status code from the request"""
        return requests.get(uri, params=params, timeout=timeout).status_code if uri else None

    @staticmethod
    def get_actual_values(uri, params, timeout, json_test):
        """Get the values from the request"""
        response = requests.get(uri, params=params, timeout=timeout) if uri else None
        json_path = TestCase.get_json_path(json_test) if json_test else None
        return Json.get_values_from_json(response.json(), json_path) if response and json_path else []

    @staticmethod
    def get_actual_value(uri, params, timeout, json_test):
        """Get the value from the request"""
        values = API.get_actual_values(uri, params, timeout, json_test)
        return next(iter(values or []), None)


class TestCase(object):
    """Provide test-case-related functions"""
    # the json paths in json files
    PATH_API_URI = '$.api.uri'
    PATH_API_PARAMS = '$.api.params'
    PATH_API_TIMEOUT = '$.api.timeout'
    PATH_TEST_CASES = '$.tests'

    # the json paths in $.tests
    PATH_JSON_PATH = '$.jsonpath'
    PATH_CONDITION = '$.condition'
    PATH_AGGREGATOR = '$.aggregator'
    PATH_EXPECTED_VALUE = '$.expected'

    @staticmethod
    def read_test_info(json_data):
        """Read the test information from the test case json-file"""
        uri = Json.get_value_from_json(json_data, TestCase.PATH_API_URI)
        params = Json.get_value_from_json(json_data, TestCase.PATH_API_PARAMS)
        timeout = Json.get_value_from_json(json_data, TestCase.PATH_API_TIMEOUT)
        json_test_cases = Json.get_value_from_json(json_data, TestCase.PATH_TEST_CASES)

        return uri, params, timeout, json_test_cases

    @staticmethod
    def get_json_path(json_test):
        """Get the json path from the json-test object"""
        return Json.get_value_from_json(json_test, TestCase.PATH_JSON_PATH)

    @staticmethod
    def get_expected_value(json_test):
        """Get the expected value from the json-test object"""
        return Json.get_value_from_json(json_test, TestCase.PATH_EXPECTED_VALUE)

    @staticmethod
    def get_condition(json_test):
        """Get the condition from the json-test object"""
        return Json.get_value_from_json(json_test, TestCase.PATH_CONDITION)

    @staticmethod
    def get_aggregator(json_test):
        """Get the aggregator from the json-test object"""
        return Json.get_value_from_json(json_test, TestCase.PATH_AGGREGATOR)
