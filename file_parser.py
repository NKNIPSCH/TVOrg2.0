import os
import re
from config import REGEX_PATTERNS

# Regex to match typical "ShowName S01E02" or "ShowName.S01E02" patterns.
TV_PATTERN = re.compile(
    r"""(?ix)            # Case-insensitive, verbose
    ^(.*?)               # 1) Capture everything (lazy) up to S##E## as show name
    [.\s_-]*             # Some optional separator (dot, space, underscore, dash)
    S(\d{1,2})           # 2) 'S' + season number (1-2 digits)
    [.\s_-]*             # More optional separators
    E(\d{1,2})           # 3) 'E' + episode number (1-2 digits)
    """,
    flags=0
)

def parse_filename(file_path):
    """
    Extract metadata from a file name, including possible show title + season/episode,
    as well as categories from config.py patterns.
    """
    filename = os.path.basename(file_path)
    metadata = {
        "filename": filename,
        "categories": [],
        "tv_show": None,
        "season": None,
        "episode": None,
        "is_duplicate": False
    }

    # ------------------------------------------------------
    # 1) Attempt to parse standard TV naming: Title SxxEyy
    tv_match = TV_PATTERN.search(filename)
    if tv_match:
        raw_show_name = tv_match.group(1)
        season_str = tv_match.group(2)
        episode_str = tv_match.group(3)

        # Clean up the show name: remove extra dots/underscores
        # For example: "Show.Name" -> "Show Name"
        cleaned_show_name = re.sub(r"[._-]+", " ", raw_show_name).strip()

        metadata["tv_show"] = cleaned_show_name
        metadata["season"] = int(season_str)
        metadata["episode"] = int(episode_str)
        metadata["categories"].append("TV Shows")
    # ------------------------------------------------------

    # 2) Match filename against predefined categories
    for category, pattern in REGEX_PATTERNS.items():
        if re.search(pattern, filename):
            metadata["categories"].append(category)

    # 3) If it's not classified as a TV show, assume it's a movie unless marked as Sports
    if not metadata["tv_show"]:
        if "Sports" in metadata["categories"]:
            metadata["categories"].append("Sports")
        else:
            metadata["categories"].append("Movies")

    # 4) If no category matches, mark it as unsorted
    if not metadata["categories"]:
        metadata["categories"].append("unsorted")

    return metadata

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = parse_filename(sys.argv[1])
        print(result)
    else:
        print("Please provide a file name to parse.")
