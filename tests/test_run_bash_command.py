import unittest
from importer.run_bash_command import runrealcmd
from unittest.mock import patch
import tempfile
import os

class Testrunrealcmd(unittest.TestCase):
    def setUp(self):
        self.stdout_mock = tempfile.NamedTemporaryFile(delete=False)

    def tearDown(self):
        self.stdout_mock.close()
        os.remove(self.stdout_mock.name)

    def test_get_filepaths(self):
        with patch("importer.run_bash_command.Popen") as mock_popen:
            self.stdout_mock.write(b"""XX:YY.H IDE interface: IIIIIIIIIIIIIIII
            XX:YY.H SMBus: BBBBBBBBBBBBBBBB
            XX:YY.H IDE interface: IIIIIIIIIIIIIIII
            XX:YY.H VGA compatible controller: GPU-MODEL-NAME
            XX:YY.H Audio device: DDDDDDDDDDDDDDDD
            XX:YY.H IDE interface: IIIIIIIIIIIIIIII
            """)
            mock_popen.return_value.stdout = self.stdout_mock
            process = mock_popen.return_value.__enter__.return_value
            process.returncode = 0
            process.communicate.return_value = (b'some output', b'some error')
            command = 'mock command'
            runrealcmd(command)
        mock_popen.assert_called_once_with('mock command', bufsize=1, close_fds=True, shell=True, stderr=-2, stdout=-1)