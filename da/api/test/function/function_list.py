from da.api.test.function.function_numeric import examine_numeric
from da.api.test.exceptions import UnsupportedAggregatorError, UnsupportedConditionError


def examine_list(self, actual_list, expected, aggregator, condition):
    """Examine the list with aggregator (e.g., length) and condition"""
    examine_aggregation_functions = {
        'length': examine_length,
        'inner-list-length': examine_inner_list_length,
        'max': examine_max,
        'min': examine_min,
        'all': examine_all
    }

    examine_condition_functions = {
        'in': examine_in
    }

    self.assertIsNotNone(aggregator or condition, 'Either aggregator or condition should be set.')

    if aggregator:
        if aggregator not in examine_aggregation_functions.keys():
            raise UnsupportedAggregatorError('Unsupported aggregator: %s' % aggregator)
        else:
            examine_aggregation_functions[aggregator](self, actual_list, expected, condition)

    elif condition not in examine_condition_functions.keys():
        raise UnsupportedConditionError('Unsupported condition type: %s' % condition)
    else:
        examine_condition_functions[condition](self, actual_list, expected)


def examine_in(self, actual_list, expected):
    self.assertIn(expected, actual_list)


def examine_length(self, actual_list, expected, condition):
    examine_numeric(self, len(actual_list), expected, condition, 'in the examination of the length of list')


def examine_inner_list_length(self, actual_list, expected, condition):
    for inner_list in actual_list:
        examine_length(self, inner_list, expected, condition)


def examine_max(self, actual_list, expected, condition):
    examine_numeric(self, max(actual_list), expected, condition, 'in the examination of the maximum value of list')


def examine_min(self, actual_list, expected, condition):
    examine_numeric(self, min(actual_list), expected, condition, 'in the examination of the minimum value of list')


def examine_all(self, actual_list, expected, condition):
    for item in actual_list:
        examine_numeric(self, item, expected, condition, 'in the examination of all the items in list')
