import unittest
from unittest.mock import patch
import sys
import main

class TestCommandLineArguments(unittest.TestCase):
    def test_missing_arguments(self):
        with patch.object(sys, "argv", ["main.py", "source_folder"]):
            with self.assertRaises(SystemExit):
                main.validate_args()

    def test_valid_arguments(self):
        with patch.object(sys, "argv", ["main.py", "source_folder", "replica_folder", "10"]):
            try:
                main.validate_args()
            except SystemExit:
                self.fail("validate_args() called sys.exit() on valid arguments!")
