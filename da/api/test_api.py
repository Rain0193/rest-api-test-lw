import glob
import json
import os
import copy
import unittest
import sys

from da.api.test import helper
from da.api.test.function import function_unittest
from da.api.test.exceptions import UnsupportedTestTypeError


class TestsContainer(unittest.TestCase):
    """The test container for dynamically generated test cases."""
    longMessage = True


def identify_files_in_dir(path):
    """Identify the json files in the given directory recursively."""
    return [target for file_path in os.walk(path) for target in glob.glob(os.path.join(file_path[0], '*.json'))]


def generate_parameter_list(params):
    """Generate the list of parameters so that not to make"""
    list_param_keys = [key for key in params.keys() if type(params[key]) is list]
    if len(list_param_keys) <= 0:
        return [params]

    if len(list_param_keys) > 1:
        return []

    list_param_key = list_param_keys[0]
    param_list = []
    for value in params[list_param_key]:
        curr_params = copy.deepcopy(params)
        curr_params[list_param_key] = value
        param_list.append(curr_params)

    return param_list


def generate_test_function_name(file_name, index_test, index_param):
    """Test function name should start with 'test' since we use unit test."""
    return 'test_%s_t%03d_p%03d' % (file_name, index_test, index_param)


if __name__ == '__main__':
    # Read test_suites_dir from the arguments.
    try:
        script, test_suites_dir = sys.argv
    except ValueError:
        print 'Please specify the test suite directory for testing.'
        raise

    for test_cases_path in identify_files_in_dir(test_suites_dir):
        print 'Working on %s ...' % test_cases_path

        try:
            json_file = open(test_cases_path)
            json_data = json.load(json_file)
        except Exception as e:
            print str(e) + ' Cannot parse the json file: "%s".' % test_cases_path
            continue

        uri, params, timeout, json_test_cases = helper.TestCase.read_test_info(json_data)
        if not uri or not timeout or not json_test_cases:
            print 'Essential test information is missing.'
            continue

        param_list = generate_parameter_list(params or {})
        if len(param_list) <= 0:
            print 'More than two lists are not allowed as parameters.'
            continue

        file_name = os.path.basename(test_cases_path)
        index_test = 1
        for json_test_case in json_test_cases:
            index_param = 1
            for param in param_list:
                test_function_name = generate_test_function_name(file_name, index_test, index_param)
                try:
                    # Make test functions dynamically
                    test_function = function_unittest.make_test_function(uri, param, timeout, json_test_case)
                    setattr(TestsContainer, test_function_name, test_function)
                    print '%s is added to the test container.' % test_function_name
                except UnsupportedTestTypeError as e:
                    print str(e) + ' at "%s" in "%s"' % (test_function_name, test_cases_path)

                index_param += 1
            index_test += 1

    suite = unittest.makeSuite(TestsContainer)
    unittest.TextTestRunner(verbosity=1).run(suite)
