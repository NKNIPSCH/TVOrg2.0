#!/usr/bin/env python3
import os
import shutil
import re
import argparse

from file_discovery import get_file_list
from config import REGEX_PATTERNS

# Import the single-pass organize_file function
from organizer import organize_file

def move_file(file_path, dest_folder, dry_run=False):
    os.makedirs(dest_folder, exist_ok=True)
    dest_file = os.path.join(dest_folder, os.path.basename(file_path))
    if dry_run:
        print(f"[Dry-run] Would move: {file_path} -> {dest_file}")
    else:
        shutil.move(file_path, dest_file)
        print(f"Moved: {file_path} -> {dest_file}")

def organize_in_stages(source, target, dry_run):
    # Get list of all files from the source directory.
    all_files = get_file_list(source)
    remaining_files = all_files.copy()

    # Counters for summary reporting.
    counts = {"NFL": 0, "Documentaries": 0, "TV Shows": 0, "Other": 0}

    # --- Pass 1: NFL Games ---
    nfl_pattern = REGEX_PATTERNS.get("NFL", r"(?i)\bNFL\b")
    ravens_pattern = REGEX_PATTERNS.get("Ravens", r"(?i)\bRavens?\b")
    for file_path in all_files:
        base = os.path.basename(file_path)
        if re.search(nfl_pattern, base) or re.search(ravens_pattern, base):
            dest = os.path.join(target, "NFL")
            if re.search(ravens_pattern, base):
                dest = os.path.join(dest, "Ravens")
            move_file(file_path, dest, dry_run)
            counts["NFL"] += 1
            if file_path in remaining_files:
                remaining_files.remove(file_path)
    print(f"Pass 1 (NFL): {counts['NFL']} files processed.")

    # --- Pass 2: Documentaries ---
    doc_pattern = REGEX_PATTERNS.get("Documentaries", r"(?i)\b(Documentary|Docu)\b")
    for file_path in all_files:
        base = os.path.basename(file_path)
        if re.search(doc_pattern, base):
            dest = os.path.join(target, "Documentaries")
            move_file(file_path, dest, dry_run)
            counts["Documentaries"] += 1
            if file_path in remaining_files:
                remaining_files.remove(file_path)
    print(f"Pass 2 (Documentaries): {counts['Documentaries']} files processed.")

    # --- Pass 3: TV Shows by Franchise ---
    tv_franchises = [
        "Rick and Morty",
        "Stargate",
        "Star Trek",
        "Lincoln Lawyer",
        "Engineering Catastrophes",
        "The Pacific",
        "Special Ops Lioness",
        "Three Kingdoms",
        "Foundation",
        "Genghis Khans Mongolia",
        "Halo",
        "Hells Angels Kingdom Come",
        "Paw Patrol",
        "Massive Engineering Mistakes",
        "The Mosquito Coast",
        "Kings and Queens of England"
    ]
    for file_path in all_files:
        base = os.path.basename(file_path)
        if file_path not in remaining_files:
            continue
        for franchise in tv_franchises:
            pattern = REGEX_PATTERNS.get(franchise)
            if pattern and re.search(pattern, base):
                dest = os.path.join(target, franchise)
                move_file(file_path, dest, dry_run)
                counts["TV Shows"] += 1
                remaining_files.remove(file_path)
                break
    print(f"Pass 3 (TV Shows): {counts['TV Shows']} files processed.")

    # --- Pass 4: Other ---
    for file_path in remaining_files:
        dest = os.path.join(target, "Other")
        move_file(file_path, dest, dry_run)
        counts["Other"] += 1
    print(f"Pass 4 (Other): {counts['Other']} files processed.")

    # --- Summary ---
    total = counts["NFL"] + counts["Documentaries"] + counts["TV Shows"] + counts["Other"]
    print("\n--- Summary ---")
    print(f"Total files processed: {total}")
    print(f"NFL: {counts['NFL']}")
    print(f"Documentaries: {counts['Documentaries']}")
    print(f"TV Shows: {counts['TV Shows']}")
    print(f"Other: {counts['Other']}")

def single_pass_organizer(source, target, dry_run):
    """
    Fallback single-pass approach: simply iterate through every file
    and call the 'organize_file' function from organizer.py.
    """
    all_files = get_file_list(source)
    print(f"\nRunning single-pass organizer on {len(all_files)} files...")
    for file_path in all_files:
        organize_file(file_path, target, dry_run=dry_run)

def main():
    parser = argparse.ArgumentParser(description="Organize TV files with staged passes.")
    parser.add_argument("source", help="Source directory containing TV files")
    parser.add_argument("target", help="Target base directory for organized files")
    parser.add_argument("--dry-run", action="store_true", help="Simulate moves without actually moving files")
    parser.add_argument("--staged", action="store_true", help="Use staged organization passes")
    args = parser.parse_args()

    if args.staged:
        organize_in_stages(args.source, args.target, args.dry_run)
    else:
        # Fallback to single-pass organizer
        single_pass_organizer(args.source, args.target, args.dry_run)

if __name__ == "__main__":
    main()
