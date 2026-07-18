"""
file_handler.py
---------------
Handles saving and loading student records using JSON file storage.
All file operations are wrapped in exception handling so the app
never crashes because of a missing or corrupted file.
"""

import json
import os

DATA_FILE = "students_data.json"


def save_to_file(students, filename=DATA_FILE):
    """
    Save a list of Student objects to a JSON file.

    Returns
    -------
    (True, success_message) or (False, error_message)
    """
    try:
        data = [s.to_dict() for s in students]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return True, f"Data saved successfully to '{filename}'."
    except PermissionError:
        return False, f"Permission denied: cannot write to '{filename}'."
    except Exception as e:
        return False, f"Error saving data: {e}"


def load_from_file(filename=DATA_FILE):
    """
    Load student records from a JSON file.

    Returns
    -------
    (list_of_dicts, message_string)
    list_of_dicts is empty if the file does not exist or cannot be parsed.
    """
    if not os.path.exists(filename):
        return [], f"No data file found ('{filename}'). Starting with empty records."

    try:
        with open(filename, "r") as f:
            content = f.read().strip()

        if not content:
            return [], f"Data file '{filename}' is empty."

        data = json.loads(content)

        if not isinstance(data, list):
            return [], "Data file format is invalid (expected a list of records)."

        return data, f"Loaded {len(data)} record(s) from '{filename}'."

    except json.JSONDecodeError:
        return [], f"Data file '{filename}' is corrupted or not valid JSON."
    except PermissionError:
        return [], f"Permission denied: cannot read '{filename}'."
    except Exception as e:
        return [], f"Error loading data: {e}"
