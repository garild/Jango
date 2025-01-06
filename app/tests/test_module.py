"""
Test Calculator functions
"""

from django.test import SimpleTestCase

from app import calculator

class TestCalculator(SimpleTestCase):
    "Test the class calculator"
    def test_add_two_numbers(self):
        result = calculator.add(2,3)
        self.assertEqual(result, 5)

    def test_subtract_two_numbers(self):
        result = calculator.sub(5,2)
        self.assertEqual(result, 3)

    def test_multiple_numbers(self):
        "Test case will multiply 2 numbers"
        result = calculator.multiply(2,3)
        self.assertEquals(result, 6)