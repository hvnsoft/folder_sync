import os
import shutil
import time
import argparse
import logging
import sys

def synchronize_folders(source_folder, replica_folder, log_file):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            logger.error(f"Source folder '{source_folder}' does not exist.")
            return
        
        # Create replica folder if it doesn't exist
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        # Loop through files and folders in source folder
        for root, dirs, files in os.walk(source_folder):
            for dir in dirs:
                source_dir_path = os.path.join(root, dir)
                replica_dir_path = os.path.join(replica_folder, os.path.relpath(source_dir_path, source_folder))
                
                # Create replica directory if it doesn't exist
                if not os.path.exists(replica_dir_path):
                    os.makedirs(replica_dir_path)
                    logger.info(f"Created folder '{replica_dir_path}'")

            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))

                # Check if the file already exists in replica folder with the same content
                if os.path.exists(replica_file_path):
                    with open(source_file_path, 'rb') as source_file, open(replica_file_path, 'rb') as replica_file:
                        if source_file.read() == replica_file.read():
                            continue  # Skip if content is identical

                # Copy file from source to replica folder
                shutil.copy2(source_file_path, replica_file_path)
                logger.info(f"Copied '{source_file_path}' to '{replica_file_path}'")

        # Loop through files in replica folder and remove any files not present in source folder
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))

                # Remove file from replica folder if it doesn't exist in source folder
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    logger.info(f"Removed '{replica_file_path}'")

        # Loop through folders in replica folder and remove any folders not present in source folder
        for root, dirs, _ in os.walk(replica_folder):
            for dir in dirs:
                replica_subfolder_path = os.path.join(root, dir)
                source_subfolder_path = os.path.join(source_folder, os.path.relpath(replica_subfolder_path, replica_folder))

                # Remove folder from replica folder if it doesn't exist in source folder
                if not os.path.exists(source_subfolder_path):
                    shutil.rmtree(replica_subfolder_path)
                    logger.info(f"Removed folder '{replica_subfolder_path}'")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Folder Synchronization Program')
    parser.add_argument('-s', '--source', type=str, default='source', help='Source folder name (default: source)')
    parser.add_argument('-r', '--replica', type=str, default='replica', help='Replica folder name (default: replica)')
    parser.add_argument('-i', '--interval', type=int, default=60, help='Synchronization interval in seconds (default: 60)')
    parser.add_argument('-l', '--log_file', type=str, default='sync.log', help='Log file name (default: sync.log)')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(filename=args.log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    global logger
    logger = logging.getLogger()

    # Add a stream handler to output log messages to the console
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    source_folder = os.path.join(os.getcwd(), args.source)
    replica_folder = os.path.join(os.getcwd(), args.replica)

    # Check if source folder exists
    if not os.path.exists(source_folder):
        logger.error(f"Source folder '{source_folder}' does not exist.")
        sys.exit(True)

    while True:
        synchronize_folders(source_folder, replica_folder, args.log_file)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()