import unittest
from main import validate_sync_time

class ValidTimeTest(unittest.TestCase):
    def test_entered_sync_time(self):
        self.assertEqual(validate_sync_time("5"), 5)
        self.assertEqual(validate_sync_time("60"), 60)
        self.assertEqual(validate_sync_time("3000"), 3000)

    def test_negativ_entered_sync_time(self):
        with self.assertRaisesRegex(ValueError,"The time value must be a number and must not be less than or equal to 0."):
            validate_sync_time("-10")

    def test_zero_entered_sync_time(self):
        with self.assertRaisesRegex(ValueError,"The time value must be a number and must not be less than or equal to 0."):
            validate_sync_time("0")

    def test_non_numeric_entered_sync_time(self):
        with self.assertRaisesRegex(ValueError,"The time value must be a number and must not be less than or equal to 0."):
            validate_sync_time("blabla")
        with self.assertRaisesRegex(ValueError,"The time value must be a number and must not be less than or equal to 0."):
            validate_sync_time("50.5")
        with self.assertRaisesRegex(ValueError,"The time value must be a number and must not be less than or equal to 0."):
            validate_sync_time("!!!")


    def test_missing_argument_sync_time(self):
        with self.assertRaisesRegex(ValueError,"Sync time is missing"):
            validate_sync_time(None)


if __name__ == '__main__':
    unittest.main()