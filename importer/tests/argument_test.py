import argparse
import unittest
from unittest.mock import Mock

from importer.argument_parser import ArgumentParser


class TestArguments(unittest.TestCase):

    def setUp(self):
        self.validation_function = Mock()
        self.under_test = ArgumentParser(self.validation_function)

    def test_should_parse_valid_arguments_to_validate_command(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i"])
        expected = argparse.Namespace(execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=True)
        self.assertEquals(actual, expected)

    def test_should_parse_when_not_part_of_internal_study(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls"])
        expected = argparse.Namespace(execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=False)
        self.assertEquals(actual, expected)

    def test_spreadsheet_is_mandatory_for_validate_command(self):
        actual = self.under_test.parse(["validate", "-i"])
        self.assertEquals(actual, None)
