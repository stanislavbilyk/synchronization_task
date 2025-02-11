import unittest
from main import ChangeFolderStatus

class ChangeFolderTest(unittest.TestCase):
    def test_init_object(self):
        source_folder = "test_source"
        replica_folder = "test_replica"
        check_folder = ChangeFolderStatus(source_folder, replica_folder)
        self.assertEqual(check_folder.source, "test_source")
        self.assertEqual(check_folder.replica, "test_replica")


    def test_missing_argument(self):
        with self.assertRaises(ValueError):
            ChangeFolderStatus(None, "test_replica")
        with self.assertRaises(ValueError):
            ChangeFolderStatus("test_source", None)
        with self.assertRaises(ValueError):
            ChangeFolderStatus(None, None)


if __name__ == '__main__':
    unittest.main()