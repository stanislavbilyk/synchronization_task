import os
import shutil
import unittest
import tempfile
from main import ChangeFolderStatus, hash_file


class TestSyncFunctionality(unittest.TestCase):
    def test_create_and_delete_folders(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
            check_folder = ChangeFolderStatus(source, replica)

            os.makedirs(os.path.join(source, "folder_1"))
            os.makedirs(os.path.join(source, "folder_1/subfolder_1"))
            os.makedirs(os.path.join(source, "folder_2"))

            for root, dirs, _ in os.walk(check_folder.source):
                rel_path = os.path.relpath(root, check_folder.source)

                replica_root = os.path.join(check_folder.replica, rel_path)
                os.makedirs(replica_root, exist_ok=True)

            self.assertTrue(os.path.exists(os.path.join(replica, "folder_1")))
            self.assertTrue(os.path.exists(os.path.join(replica, "folder_1/subfolder_1")))
            self.assertTrue(os.path.exists(os.path.join(replica, "folder_2")))

            empty_folder = os.path.join(replica, "empty_folder")
            os.makedirs(empty_folder)
            self.assertTrue(os.path.exists(empty_folder))

            os.rmdir(empty_folder)
            self.assertFalse(os.path.exists(empty_folder))

    def test_file_copies_if_hash_changes(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
            check_folder = ChangeFolderStatus(source, replica)

            source_file = os.path.join(source, "test.txt")
            replica_file = os.path.join(replica, "test.txt")

            with open(source_file, "w") as f:
                f.write("test data")

            shutil.copy2(source_file, replica_file)

            self.assertEqual(hash_file(source_file), hash_file(replica_file))

            with open(source_file, "w") as f:
                f.write("new test data")

            self.assertNotEqual(hash_file(source_file), hash_file(replica_file))

            check_folder.create("test.txt")

            self.assertEqual(hash_file(source_file), hash_file(replica_file))

    def test_file_does_not_copy_if_hash_unchanged(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
            check_folder = ChangeFolderStatus(source, replica)

            source_file = os.path.join(source, "test.txt")
            replica_file = os.path.join(replica, "test.txt")

            with open(source_file, "w") as f:
                f.write("test data")

            shutil.copy2(source_file, replica_file)

            self.assertEqual(hash_file(source_file), hash_file(replica_file))

            last_modified_before = os.path.getmtime(replica_file)

            check_folder.create("test.txt")

            last_modified_after = os.path.getmtime(replica_file)
            self.assertEqual(last_modified_before, last_modified_after)


    def test_create_files(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
            check_folder = ChangeFolderStatus(source, replica)

            source_file = os.path.join(source, "test.txt")
            check_folder.create(source_file)

            self.assertTrue(os.path.exists(source_file))

    def test_delete_missing_files(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
            check_folder = ChangeFolderStatus(source, replica)

            replica_file = os.path.join(replica, "test.txt")
            with open(replica_file, "w") as f:
                f.write("test data")

            check_folder.delete("test.txt")

            self.assertFalse(os.path.exists(replica_file))


if __name__ == "__main__":
    unittest.main()
