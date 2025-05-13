import unittest
from src.commands.command_parser import CommandParser
import pandas as pd


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'Los Angeles', 'Chicago']
        })
        pass

    def test_generate_command(self):
        parser = CommandParser()
        with self.assertRaises(ValueError) as context:
            parser.parse("gen")

        self.assertEqual(
            str(context.exception),
            "Generate command requires a variable name and expression."
        )

        desired_output = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'Los Angeles', 'Chicago'],
            'age_squared': [625, 900, 1225]
        })

        self.assertEqual(desired_output, parser.parse("gen age_squared age ** 2"))


