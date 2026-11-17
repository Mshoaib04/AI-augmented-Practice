import unittest

from calculator import calculator


class CalculatorTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculator("add", 3, 4), 7)

    def test_subtraction(self):
        self.assertEqual(calculator("subtract", 9, 4), 5)

    def test_multiplication(self):
        self.assertEqual(calculator("multiply", 3, 4), 12)

    def test_division(self):
        self.assertEqual(calculator("divide", 9, 3), 3)

    def test_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "divide by zero"):
            calculator("divide", 9, 0)

    def test_invalid_operation(self):
        with self.assertRaisesRegex(ValueError, "Unsupported operation"):
            calculator("power", 2, 3)


if __name__ == "__main__":
    unittest.main()