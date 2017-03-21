from da.api.test.exceptions import UnsupportedConditionError


def examine_string(self, actual, expected, condition):
    """Examine the string value with condition"""
    examine_functions = {
        'exact': examine_string_exact,
        'contains': examine_string_contains,
        'startswith': examine_string_startswith,
        'endswith': examine_string_endswith
    }

    if condition not in examine_functions.keys():
        raise UnsupportedConditionError('Unsupported condition type: %s' % condition)

    examine_functions[condition](self, actual, expected)


def examine_string_exact(self, actual, expected):
    self.assertEqual(expected, actual)


def examine_string_contains(self, actual, expected):
    self.assertIn(expected, actual)


def examine_string_startswith(self, actual, expected):
    self.assertTrue(actual.startswith(expected), '"%s" does not start with "%s".' % (actual, expected))


def examine_string_endswith(self, actual, expected):
    self.assertTrue(actual.endswith(expected), '"%s" does not end with "%s".' % (actual, expected))
