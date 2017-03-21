class UnsupportedTestTypeError(Exception):
    """Test types are not supported"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class UnsupportedConditionError(Exception):
    """Conditions are not supported"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class UnsupportedAggregatorError(Exception):
    """Aggregators are not supported"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
