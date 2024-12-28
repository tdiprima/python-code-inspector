import unittest
import my_module

class TestMy_module(unittest.TestCase):
    def test_calculate_sum(self):
        # TODO: Add appropriate test cases
        result = my_module.calculate_sum(None)
        self.assertIsNotNone(result)