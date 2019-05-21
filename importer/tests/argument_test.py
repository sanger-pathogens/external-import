import argparse
import unittest
from unittest.mock import Mock

from importer.argument_parser import ArgumentParser


class TestValidateCommandArguments(unittest.TestCase):

    def setUp(self):
        self.validation_function = Mock()
        self.under_test = ArgumentParser(self.validation_function)

    def test_should_parse_valid_arguments(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i", "-o", "output"])
        expected = argparse.Namespace(output='output', execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=True)
        self.assertEqual(actual, expected)

    def test_should_parse_when_not_part_of_internal_study(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-o", "output"])
        expected = argparse.Namespace(output='output', execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=False)
        self.assertEqual(actual, expected)

    def test_spreadsheet_is_mandatory(self):
        actual = self.under_test.parse(["validate", "-i", "-o", "output"])
        self.assertEqual(actual, None)

    def test_output_is_mandatory(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i"])
        self.assertEqual(actual, None)
