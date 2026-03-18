import pytest

def factorial(n):
    if type(n) is not int or n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@pytest.mark.parametrize("input_val, expected", [
    (0, 1),
    (1, 1),
    (5, 120)
])
def test_valid_factorial(input_val, expected):
    assert factorial(input_val) == expected

@pytest.mark.parametrize("input_val", [-3, 1.5, False, 'abc'])
def test_invalid_factorial(input_val):
    assert factorial(input_val) is None