import argparse
import unittest
from unittest.mock import Mock

from importer.argument_parser import ArgumentParser


class TestValidateCommandArguments(unittest.TestCase):

    def setUp(self):
        self.validation_function = Mock()
        self.under_test = ArgumentParser(self.validation_function)

    def test_should_parse_valid_arguments_copy(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i", "-o", "output", "-cp"])
        expected = argparse.Namespace(copy=True, download=False, output='output', execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=True)
        self.assertEqual(actual, expected)

    def test_should_parse_valid_arguments_download(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-i", "-o", "output", "-dl"])
        expected = argparse.Namespace(copy=False, download=True, output='output', execute=self.validation_function, spreadsheet="test_upload.xls",
                                      part_of_internal_study=True)
        self.assertEqual(actual, expected)

    def test_should_parse_when_not_part_of_internal_study(self):
        actual = self.under_test.parse(["validate", "-s", "test_upload.xls", "-o", "output", "-cp"])
        expected = argparse.Namespace(copy=True, download=False, output='output', execute=self.validation_function, spreadsheet="test_upload.xls",
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

    def test_should_parse_valid_arguments_copy_input(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123"])
        expected = argparse.Namespace(output='output', input='input', execute=self.preparation_function,
                                      spreadsheet="test_upload.xls", ticket=123, connections=10, download=False)
        self.assertEqual(actual, expected)

    def test_should_parse_valid_arguments_download_ENA(self):
        actual = self.under_test.parse(["prepare", "-dl", "-c", "50", "-s", "test_upload.xls", "-o", "output", "-t", "123"])
        expected = argparse.Namespace(output='output', input=None, execute=self.preparation_function,
                                      spreadsheet="test_upload.xls", ticket=123, connections=50,
                                      download=True)
        self.assertEqual(actual, expected)

    def test_spreadsheet_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-i", "input", "-o", "output", "-t", "123"])
        self.assertIsNone(actual)

    def test_input_or_download_is_mandatory(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-o", "output", "-t", "123"])
        self.assertIsNone(actual)

    def test_input_and_download_not_allowed(self):
        actual = self.under_test.parse(["prepare", "-i", "input", "-dl", "-s", "test_upload.xls", "-o", "output", "-t", "123"])
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

    def test_connections_is_a_number(self):
        actual = self.under_test.parse(
            ["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123", "-c", "invalid_number_of_connections"])
        self.assertIsNone(actual)

    def test_connections_defaults_to_10(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123"])
        expected = argparse.Namespace(output='output', input='input', execute=self.preparation_function,
                                      spreadsheet="test_upload.xls", ticket=123, connections=10, download=False)
        self.assertEqual(actual, expected)

    def test_connections_cant_be_0(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123", "-b","10","-c","0"])
        expected = None
        self.assertEqual(actual, expected)

    def test_connections_cant_be_greater_than_1000(self):
        actual = self.under_test.parse(["prepare", "-s", "test_upload.xls", "-i", "input", "-o", "output", "-t", "123", "-b","10","-c","1001"])
        expected = None
        self.assertEqual(actual, expected)


class TestImportCommandArguments(unittest.TestCase):

    def setUp(self):
        self.import_function = Mock()
        self.under_test = ArgumentParser(load=self.import_function)

    def test_should_parse_valid_arguments(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-o", "output", "-t", "123", "-c", "commands_dir","-b","10"])
        expected = argparse.Namespace(output='output', database='a_database', commands='commands_dir',
                                      execute=self.import_function, ticket=123, breakpoint=10)
        self.assertEqual(actual, expected)

    def test_breakpoint_defaults_to_0(self):
        actual = self.under_test.parse(["load", "-d", "a_database", "-o", "output", "-t", "123", "-c", "commands_dir"])
        expected = argparse.Namespace(output='output', database='a_database', commands='commands_dir',
                                      execute=self.import_function, ticket=123, breakpoint=0)
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
