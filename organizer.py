import os
import shutil
from file_parser import parse_filename
from file_discovery import get_file_list
from logger_util import log_action
from tqdm import tqdm

def determine_destination(metadata, target_base):
    """
    Determine the destination folder based on the file's metadata.
    Ensures that folder names remain unchanged while files are moved within their existing directories.
    """
    categories = metadata.get("categories", [])
    show_name = metadata.get("tv_show")
    season = metadata.get("season")

    dest_folder = target_base

    # Maintain existing folder names and structure while reorganizing
    original_folder = os.path.dirname(metadata.get("original_path", ""))

    # If a TV show is detected, organize under TV Shows
    if show_name:
        show_folder = os.path.join(dest_folder, "TV Shows", show_name)
        if season:
            season_folder = f"Season {season:02d}"  # e.g., "Season 01"
            dest_folder = os.path.join(show_folder, season_folder)
        else:
            dest_folder = show_folder
    else:
        # Handle categorization without altering folder names
        if "NFL" in categories:
            dest_folder = os.path.join(dest_folder, "NFL")
            if "Ravens" in categories:
                dest_folder = os.path.join(dest_folder, "Ravens")
        elif "World Series of Poker" in categories:
            dest_folder = os.path.join(dest_folder, "World Series of Poker")
        elif "Documentaries" in categories:
            dest_folder = os.path.join(dest_folder, "Documentaries")
        elif "unsorted" in categories:
            dest_folder = os.path.join(dest_folder, "Unsorted")
        else:
            if categories:
                dest_folder = os.path.join(dest_folder, categories[0])
            else:
                dest_folder = os.path.join(dest_folder, "Unsorted")

    # Preserve existing folder names, only move files
    if original_folder:
        dest_folder = os.path.join(dest_folder, os.path.basename(original_folder))

    return dest_folder

def organize_file(file_path, target_base, dry_run=False):
    """
    Organize a single file:
      - Parse its metadata
      - Determine the destination folder while preserving folder names
      - Move the file
    """
    metadata = parse_filename(file_path)
    metadata["original_path"] = file_path  # Store original path for reference
    dest_folder = determine_destination(metadata, target_base)

    if not dry_run:
        os.makedirs(dest_folder, exist_ok=True)

    dest_file_path = os.path.join(dest_folder, os.path.basename(file_path))

    if dry_run:
        print(f"[Dry-run] Would move: {file_path} -> {dest_file_path}")
    else:
        shutil.move(file_path, dest_file_path)
        log_action(f"Moved: {file_path} -> {dest_file_path}")
        print(f"Moved: {file_path} -> {dest_file_path}")

    return dest_file_path

def remove_empty_folders(directory):
    """
    Recursively delete empty folders after reorganization.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):  # Folder is empty
                os.rmdir(folder_path)
                log_action(f"Deleted empty folder: {folder_path}")
                print(f"Deleted empty folder: {folder_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Organize TV files while preserving folder names.")
    parser.add_argument("source", help="Source directory containing the TV files.")
    parser.add_argument("target", help="Target base directory for organized files.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate moves without changing any files.")
    parser.add_argument("--cleanup", action="store_true", help="Remove empty folders after organizing.")
    args = parser.parse_args()

    # Retrieve all files from the source directory.
    files = get_file_list(args.source)
    print(f"Found {len(files)} files in '{args.source}'.")

    for file_path in tqdm(files, desc="Organizing files"):
        organize_file(file_path, args.target, dry_run=args.dry_run)

    if args.cleanup:
        remove_empty_folders(args.source)
