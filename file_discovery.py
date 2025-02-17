# file_discovery.py
import os

def get_file_list(root_directory):
    """
    Recursively scans the given root directory and returns a list of full file paths.
    """
    file_list = []
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_list.append(full_path)
    return file_list

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Recursively list files from a given directory."
    )
    parser.add_argument("root_directory", help="Directory to scan.")
    args = parser.parse_args()
    files = get_file_list(args.root_directory)
    for f in files:
        print(f)
