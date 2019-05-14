import unittest

from importer.validation import validate_study_name, validate_study_name_length
from importer.model import Spreadsheet


class TestValidation(unittest.TestCase):

    def test_study_name_with_valid_char_should_pass_validation(self):
        self.assertEqual([], validate_study_name(Spreadsheet("ValidName12345__")))

    def test_study_name_with_invalid_char_should_fail_validation(self):
        self.assertEqual(34, len(validate_study_name(Spreadsheet("!\"£$%^&*()+={}[]:@~;'#?/>.<,|\\`¬ \t"))))

    def test_study_name_of_15_chars_or_less_are_valid(self):
        self.assertEqual([], validate_study_name_length(Spreadsheet("123456789012345")))

    def test_study_name_with_invalid_char_should_fail_validation(self):
        self.assertEqual(["Spreadsheet name longer than 15 chars"], validate_study_name_length(Spreadsheet("1234567890123456")))

