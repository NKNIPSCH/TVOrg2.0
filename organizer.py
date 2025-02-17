import os
import shutil
from file_parser import parse_filename
from file_discovery import get_file_list
from logger_util import setup_logger
from tqdm import tqdm

logger = setup_logger()

def determine_destination(metadata, target_base):
    """
    Determine the destination folder based on the file's metadata.
    """
    categories = metadata.get("categories", [])
    show_name = metadata.get("tv_show")  # Possibly None
    season = metadata.get("season")      # Possibly None

    dest_folder = target_base

    if show_name:
        show_folder = os.path.join(dest_folder, "TV Shows", show_name)
        if season:
            season_folder = f"Season {season:02d}"  # e.g. "Season 01"
            dest_folder = os.path.join(show_folder, season_folder)
        else:
            dest_folder = show_folder
        return dest_folder

    if "NFL" in categories:
        dest_folder = os.path.join(dest_folder, "NFL")
        if "Ravens" in categories:
            dest_folder = os.path.join(dest_folder, "Ravens")
    elif "Stargate" in categories:
        dest_folder = os.path.join(dest_folder, "Stargate")
    elif "Star Trek" in categories:
        dest_folder = os.path.join(dest_folder, "Star Trek")
    elif "World Series of Poker" in categories:
        dest_folder = os.path.join(dest_folder, "World Series of Poker")
    elif "Documentaries" in categories:
        dest_folder = os.path.join(dest_folder, "Documentaries")
    elif "unsorted" in categories:
        dest_folder = os.path.join(dest_folder, "unsorted")
    else:
        if categories:
            dest_folder = os.path.join(dest_folder, categories[0])
        else:
            dest_folder = os.path.join(dest_folder, "unsorted")

    return dest_folder

def organize_file(file_path, target_base, dry_run=False):
    """
    Organize a single file.
    """
    metadata = parse_filename(file_path)
    dest_folder = determine_destination(metadata, target_base)

    if not dry_run:
        os.makedirs(dest_folder, exist_ok=True)

    dest_file_path = os.path.join(dest_folder, os.path.basename(file_path))
    if dry_run:
        print(f"[Dry-run] Would move: {file_path} -> {dest_file_path}")
    else:
        shutil.move(file_path, dest_file_path)
        logger.info(f"Moved: {file_path} -> {dest_file_path}")
        print(f"Moved: {file_path} -> {dest_file_path}")

    return dest_file_path

def remove_empty_folders(directory):
    """
    Recursively delete empty folders after organizing.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for d in dirs:
            folder_path = os.path.join(root, d)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                logger.info(f"Deleted empty folder: {folder_path}")
                print(f"Deleted empty folder: {folder_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Organize TV files based on metadata."
    )
    parser.add_argument("source", help="Source directory containing the TV files.")
    parser.add_argument("target", help="Target base directory for organized files.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate moves without changing any files.")
    args = parser.parse_args()

    files = get_file_list(args.source)
    print(f"Found {len(files)} files in '{args.source}'.")

    for file_path in tqdm(files, desc="Organizing files"):
        organize_file(file_path, args.target, dry_run=args.dry_run)

    if not args.dry_run:
        remove_empty_folders(args.source)
