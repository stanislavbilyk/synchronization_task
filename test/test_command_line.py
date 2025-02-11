import unittest
from unittest.mock import patch
import sys
import main

class TestCommandLineArguments(unittest.TestCase):
    @patch('main.sync_folders')
    def test_missing_arguments(self, mock_sync):
        with patch.object(sys, "argv", ["main.py", "source_folder"]):
            with self.assertRaises(SystemExit):
                main.validate_args()

    @patch('main.sync_folders')
    def test_valid_arguments(self, mock_sync):
        with patch.object(sys, "argv", ["main.py", "source_folder", "replica_folder", "10"]):
            try:
                main.validate_args()
            except SystemExit:
                self.fail("validate_args() called sys.exit() on valid arguments!")

if __name__ == '__main__':
    unittest.main()