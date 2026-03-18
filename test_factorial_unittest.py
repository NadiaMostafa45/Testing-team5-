import unittest

def factorial(n):
    if type(n) is not int or n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

class TestFactorial(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)

    def test_invalid_inputs(self):
        self.assertIsNone(factorial(-3))
        self.assertIsNone(factorial(1.5))
        self.assertIsNone(factorial(False))
        self.assertIsNone(factorial('abc'))

if __name__ == '__main__':
    unittest.main()