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
        self.assertIsNone(actual)

    def test_output_is_mandatory(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i"])
        self.assertIsNone(actual)


class TestPrepareCommandArguments(unittest.TestCase):

    def setUp(self):
        self.preparation_function = Mock()
        self.under_test = ArgumentParser(prepare=self.preparation_function)

    def test_should_parse_valid_arguments(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123",
                                        "-b", "456"])
        expected = argparse.Namespace(output='output', input='input', execute=self.preparation_function,
                                      spreadsheet="test_upload.xls", ticket=123, breakpoint=456)
        self.assertEqual(actual, expected)

    def test_spreadsheet_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-i", "input", "-o", "output", "-t", "123"])
        self.assertIsNone(actual)

    def test_input_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-o", "output", "-t", "123"])
        self.assertIsNone(actual)

    def test_output_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-t", "123"])
        self.assertIsNone(actual)

    def test_ticket_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output"])
        self.assertIsNone(actual)

    def test_ticket_is_a_number(self):
        actual = self.under_test.parse(
            ["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "invalid_ticket"])
        self.assertIsNone(actual)

    def test_breakpoint_is_a_number(self):
        actual = self.under_test.parse(
            ["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123", "-b", "invalid_break"])
        self.assertIsNone(actual)

    def test_breakpoint_defaults_to_0(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123"])
        expected = argparse.Namespace(output='output', input='input', execute=self.preparation_function,
                                      spreadsheet="test_upload.xls", ticket=123, breakpoint=0)
        self.assertEqual(actual, expected)


class TestImportCommandArguments(unittest.TestCase):

    def setUp(self):
        self.import_function = Mock()
        self.under_test = ArgumentParser(load=self.import_function)

    def test_should_parse_valid_arguments(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-o", "output", "-t", "123", "-c", "commands_dir"])
        expected = argparse.Namespace(output='output', database='a_database', commands='commands_dir',
                                      execute=self.import_function, ticket=123)
        self.assertEqual(actual, expected)

    def test_commands_is_mandatory(self):
        actual = self.under_test.parse(["load", "-o", "output", "-t", "123", "-d", "a_database"])
        self.assertIsNone(actual)

    def test_database_is_mandatory(self):
        actual = self.under_test.parse(["load", "-o", "output", "-t", "123", "-c", "commands_dir"])
        self.assertIsNone(actual)

    def test_output_is_mandatory(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-t", "123", "-c", "commands_dir"])
        self.assertIsNone(actual)

    def test_ticket_is_mandatory(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-o", "output", "-c", "commands_dir"])
        self.assertIsNone(actual)

    def test_ticket_is_a_number(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-o", "output", "-t", "invalid_ticket", "-c",
                                        "commands_dir"])
        self.assertIsNone(actual)
