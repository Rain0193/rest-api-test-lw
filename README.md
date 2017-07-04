# a Lightweight Testing Framework for REST API
## 1. Introduction
*rest-api-test-lw* is a lightweight testing framework for REST services. It reads test cases from JSON files, and then dynamically generates and executes unittest of Python. It currently supports HTTP GET method only. The other HTTP methods will be supported if necessary.

## 2. Getting Started
Write your test cases into JSON files and pass their locations as the argument.

### 2.1. JSON File Format
JSON files basically consist of *api* and *tests* parts. In the *api* part, you can set the target REST API by URI (*"uri"*) and parameters (*"params"*) with timeout (*"timeout"*) in seconds; parameters are optional. In *tests* part, you can add test cases.

```python
{
  "api": {
    "uri": "uri",
    "params": {
      "parameter key": "parameter value",
      ...
    },
    "timeout": "timeout in seconds"
  },
  "tests": [
    {
       "test cases"
    },
    ...
  ]
}
```

At most one parameter can have the list of values. Please refer to [jsonplaceholder.json](/da/api/testsuites/samples/jsonplaceholder.json).

### 2.2. Test Cases
Test cases require JSON path (*"jsonpath"*), condition (*"condition"*) and expected value (*"expected"*). *rest-api-test-lw* uses [jsonpath-rw](https://pypi.python.org/pypi/jsonpath-rw) to parse JSON path.

The following test case checks if the string value at *"$.url"* is equivalent to *"https://api.github.com/orgs/ridibooks"*:

```python
{
  "type": "string",
  "condition": "exact",
  "jsonpath": "$.url",
  "expected": "https://api.github.com/orgs/ridibooks"
}
```

### 2.3. Supporting Test-case Type
*rest-api-test-lw* supports the following test-case types:
* *status_code*: Checks HTTP status code.
* *string*: Checks string value.
* *numeric*: Checks integer- or float-type numeric value.
* *list*: Checks the list of string or numeric values.

% You can add a new test-case type to [function_unittest.py](/da/api/test/function/function_unittest.py).

#### 2.3.1. status_code
The *status_code* type checks if the expected HTTP status code is received.
This is an example of test cases:

```python
{
  "type": "status_code",
  "expected": 200
}
```

#### 2.3.2. string
The *string* type supports the following conditions in testing:
* *exact*: Checks if the requested value is exactly identical to the expected value. (*unittest.assertEqual* function is used.)
* *contains*: Checks if the requested value contains the expected value. (*unittest.assertIn* function is used.)
* *startswith*: Checks if the requested value starts with the expected value. (*startswith* function is used.)
* *endswith*: Checks if the requested value ends with the expected value. (*endswith* function is used.)

% You can add a new condition for the *string* type to [function_string.py](/da/api/test/function/function_string.py).

#### 2.3.3. numeric
The *numeric* type supports the following conditions in testing:
* *equal*: Checks if the requested value is equal to the expected value. (*unittest.assertAlmostEqual* function is used with 7 decimal points.)
* *less-than*: Checks if the requested value is less than the expected value. (*unittest.assertLess* function is used.)
* *greater-than*: Checks if the requested value is greater than the expected value. (*unittest.assertGreater* function is used.)
* *less-than-equal-to*: Checks if the requested value is less than or equal to the expected value. (*unittest.assertLessEqual* function is used.)
* *greater-than-equal-to*: Checks if the requested value is greater than or equal to the expected value. (*unittest.assertGreaterEqual* function is used.)
* *range*: Checks if the requested value is within the expected range including the starting and ending points.

The following test case checks if the numeric value at *"$.public_repos"* is greater than or equal to 1:

```python
{
  "type": "numeric",
  "condition": "greater-than-equal-to",
  "jsonpath": "$.public_repos",
  "expected": 1
}
```

% You can add a new condition for the *numeric* type to [function_numeric.py](/da/api/test/function/function_numeric.py).

### 2.3.4. list
Unlike the other types, the *list* type supports not only conditions but also *aggregation* methods. When using aggregation, you can apply the conditions of the numeric type. The list type supports the following aggregation methods:
* *length*: The length of the list.
* *inner-list-length*: The length of the lists inside the list.
* *max*: The maximum value from the list.
* *min*: The minimum value from the list.
* *all*: All values in the list.

The following test case checks if the length of the list at *"$[*]"* is greater than or equal to 3:
```python
{
  "type": "list",
  "aggregator": "length",
  "condition": "greater-than-equal-to",
  "jsonpath": "$[*]",
  "expected": 3
}
```

The *list* type supports the following condition (without aggregation method):
* *in*: Checks if the expected value exists in the requested list. (*unittest.assertIn* function is used.)

The following test case checks if *"namenu"* exists in the list at "$[*].login":
```python
{
  "type": "list",
  "condition": "in",
  "jsonpath": "$[*].login",
  "expected": "namenu"
}
```

% You can add a new aggregation method or condition for the *list* type to [function_list.py](/da/api/test/function/function_list.py).

### 2.4 Test-case Name
The names for test cases are automatically generated with the following format:
```python
test_"JSON file name"_t"test case order in JSON file"_p"parameter set order"
```

For example, this is the name for the 3rd test case that uses the 1st parameter set in *"test.json"* file:
```python
test_test.json_t003_p001
```

### 2.5. Run 
Pass the directory location of JSON files as the argument:
```python
python ./da/api/test_api.py "JSON file directory"
```

If your python cannot identify the *da.api.test* module then set the python path:
```python
export PYTHONPATH=.
```
