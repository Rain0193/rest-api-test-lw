from da.api.test.exceptions import UnsupportedConditionError


def examine_numeric(self, actual, expected, condition, msg=None):
    """Examine the numeric value with condition"""
    examine_functions = {
        'equal': examine_numeric_equal,
        'less-than': examine_numeric_less_than,
        'greater-than': examine_numeric_greater_than,
        'less-than-equal-to': examine_numeric_less_than_equal_to,
        'greater-than-equal-to': examine_numeric_greater_than_equal_to,
        'range': examine_numeric_range
    }

    if condition not in examine_functions.keys():
        raise UnsupportedConditionError('Unsupported condition type: %s' % condition)

    examine_functions[condition](self, float(actual), float(expected) if condition != 'range' else expected, msg)


def examine_numeric_equal(self, actual, expected, msg):
    self.assertAlmostEqual(expected, actual, msg)


def examine_numeric_less_than(self, actual, expected, msg):
    self.assertLess(actual, expected, msg)


def examine_numeric_greater_than(self, actual, expected, msg):
    self.assertGreater(actual, expected, msg)


def examine_numeric_less_than_equal_to(self, actual, expected, msg):
    self.assertLessEqual(actual, expected, msg)


def examine_numeric_greater_than_equal_to(self, actual, expected, msg):
    self.assertGreaterEqual(actual, expected, msg)


def examine_numeric_range(self, actual, expected, msg):
    self.assertTrue(float(expected[0]) <= actual <= float(expected[1]),
                    '%s is not between %s and %s %s' % (actual, float(expected[0]), float(expected[1]), msg))
