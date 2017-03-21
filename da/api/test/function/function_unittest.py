from da.api.test import helper
from da.api.test.exceptions import UnsupportedTestTypeError
from da.api.test.function.function_list import examine_list
from da.api.test.function.function_numeric import examine_numeric
from da.api.test.function.function_string import examine_string


def make_test_function(uri, params, timeout, json_test_case):
    """Make test function according to the test type"""
    def test_status_code(self):
        actual = helper.API.get_status_code(uri, params, timeout)
        expected = helper.TestCase.get_expected_value(json_test_case)

        self.assertEqual(actual, expected, 'Unexpected status code.')

    def test_string(self):
        actual = helper.API.get_actual_value(uri, params, timeout, json_test_case)
        expected = helper.TestCase.get_expected_value(json_test_case)
        condition = helper.TestCase.get_condition(json_test_case)

        examine_string(self, actual, expected, condition)

    def test_numeric(self):
        actual = helper.API.get_actual_value(uri, params, timeout, json_test_case)
        expected = helper.TestCase.get_expected_value(json_test_case)
        condition = helper.TestCase.get_condition(json_test_case)

        examine_numeric(self, actual, expected, condition)

    def test_list(self):
        actual = helper.API.get_actual_values(uri, params, timeout, json_test_case)
        expected = helper.TestCase.get_expected_value(json_test_case)
        aggregator = helper.TestCase.get_aggregator(json_test_case)
        condition = helper.TestCase.get_condition(json_test_case)

        examine_list(self, actual, expected, aggregator, condition)

    test_functions = {
        'status_code': test_status_code,
        'string': test_string,
        'numeric': test_numeric,
        'list': test_list
    }

    if json_test_case['type'] not in test_functions.keys():
        raise UnsupportedTestTypeError('Unsupported test type: %s' % json_test_case['type'])

    return test_functions[json_test_case['type']]
