# logger_util.py

import logging
import os

# Define log file location
LOG_FILE = "organizer.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_action(action, source, destination=None):
    """
    Logs an action performed by the organizer.

    :param action: Type of action (Move, Delete, Error, etc.)
    :param source: Source file/folder being affected
    :param destination: Destination file/folder (if applicable)
    """
    if destination:
        message = f"{action}: {source} -> {destination}"
    else:
        message = f"{action}: {source}"

    logging.info(message)
    print(message)  # Also print to console for real-time updates
