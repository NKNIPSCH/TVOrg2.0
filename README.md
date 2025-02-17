# TV File Organizer

## Overview

This script organizes TV-related files into structured directories based on metadata extracted from filenames. It supports detecting TV shows, documentaries, sports, and other categorized content, placing them into appropriate folders.

## Features

- **Automatic Categorization**: Sorts files into categories based on predefined patterns.
- **TV Show Organization**: Places TV shows into structured folders (`Show Name/Season XX`).
- **Dry Run Mode**: Simulates file moves before applying changes.
- **Logging**: Tracks all moves and deletions for review.
- **Undo Support**: Keeps a log of operations to allow rollbacks.
- **Automatic Cleanup**: Removes empty folders after organization.

## Requirements

- Python 3.x
- Dependencies: Install using `pip install -r requirements.txt` (if required)

## Usage

### Running in Dry-Run Mode

To simulate organization without moving files:

```bash
python3 organizer.py /path/to/source /path/to/destination --dry-run
```

### Running the Actual Organization

To move and organize files:

```bash
python3 organizer.py /path/to/source /path/to/destination
```

### Undo Last Organization

To revert the last set of file moves:

```bash
python3 undo.py
```

## Folder Structure

The script organizes files into the following hierarchy:

```
TV_Organized/
├── TV Shows/
│   ├── Show Name/
│   │   ├── Season 01/
│   │   ├── Season 02/
│   │   ├── ...
├── NFL/
│   ├── Ravens/
├── Documentaries/
├── World Series of Poker/
├── Unsorted/
```

## Logging

All operations are logged to a file for tracking and debugging. The log file is stored in the project directory.

## Deleting Empty Folders

After organization, empty folders in the source directory are automatically deleted to keep things clean.

## Customization

- Modify `config.py` to update category detection.
- Update `file_parser.py` to refine metadata extraction logic.

## Notes

- Ensure backups are in place before running.
- Undo feature works only for the last executed organization.
- Log files help in tracking moved files if manual intervention is needed.

## License

This script is provided as-is without warranty. Modify and use it as needed.


