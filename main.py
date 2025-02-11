import shutil
import sys
import logging
import os
import hashlib
import time



logging.basicConfig(level=logging.INFO, filename='synch_info.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S', encoding="utf-8")

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

class ChangeFolderStatus():
    def __init__(self, source: str, replica: str) -> None:
        if source is None:
            raise ValueError("Source folder must be provided")
        if replica is None:
            raise ValueError("Replica folder must be provided")
        self.source = source
        self.replica = replica
    def create(self, file: str) -> None:
        source_path = os.path.join(self.source, file)
        replica_path = os.path.join(self.replica, file)
        shutil.copy2(source_path, replica_path)
        logging.info(f'File {file} created in the {replica_path}')
        print(f'File {file} created in the {replica_path}')

    def delete(self, file: str) -> None:
        replica_path = os.path.join(self.replica, file)
        os.remove(replica_path)
        logging.info(f'File {file} deleted from {replica_path}')
        print(f'File {file} deleted from {replica_path}')


def hash_file(file_name: str) -> str:
    hash = hashlib.md5()
    with open(file_name, "rb") as file:
        while chunk := file.read(4096):
            hash.update(chunk)
    return hash.hexdigest()

def validate_sync_time(value: str) -> int:
    if value is None:
        raise ValueError("Sync time is missing")
    try:
        sync_time = int(value)
        if sync_time <= 0:
            raise ValueError("The time value must be a number and must not be less than or equal to 0.")
        return sync_time
    except ValueError as e:
        raise ValueError("The time value must be a number and must not be less than or equal to 0.") from e


def sync_folders(source: str, replica: str, sync_time: int) -> None:
    check_folder = ChangeFolderStatus(source, replica)
    while True:
        for root, dirs, files in os.walk(check_folder.source):
            rel_path = os.path.relpath(root, check_folder.source)
            replica_root = os.path.join(check_folder.replica, rel_path)
            os.makedirs(replica_root, exist_ok=True)
            for file in files:
                source_path = os.path.join(root, file)
                replica_path = os.path.join(replica_root, file)
                if not os.path.exists(replica_path) or hash_file(source_path) != hash_file(replica_path):
                    check_folder.create(os.path.join(rel_path, file))
                    logging.info(f'File {file} has been updated in the {rel_path}')
                    print(f"File {file} has been updated in the {rel_path}")
        for root, dirs, files in os.walk(check_folder.replica, topdown=False):
            rel_path = os.path.relpath(root, check_folder.replica)
            # source_root = os.path.join(check_folder.source, rel_path)
            for file in files:
                source_path = os.path.join(check_folder.source, rel_path, file)
                # replica_path = os.path.join(root, file)
                if not os.path.exists(source_path):
                    check_folder.delete(os.path.join(rel_path, file))
                    logging.info(f'File {file} deleted from {rel_path}')
                    print(f"File {file} deleted from {rel_path}")
            if not os.listdir(root):
                os.rmdir(root)
                logging.info(f'Empty folder {root} deleted')
                print(f"Folder {root} deleted from replica_folder")

        time.sleep(sync_time)

def validate_args() -> None:
    if len(sys.argv) < 4:
        print("Usage: python main.py <source_folder> <replica_folder> <sync_time>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    sync_time = validate_sync_time(sys.argv[3])
    print(f"Synchronization will run every {sync_time} seconds.")
    sync_folders(source_folder, replica_folder, sync_time)


if __name__ == "__main__":
    validate_args()