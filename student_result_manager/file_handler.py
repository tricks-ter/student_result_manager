import json
import os

DATA_FILE = "students_data.json"


def save_to_file(students, filename=DATA_FILE):
    try:
        data = [s.to_dict() for s in students]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return True, f"Data saved to '{filename}'."
    except PermissionError:
        return False, f"Cannot write to '{filename}', permission denied."
    except Exception as e:
        return False, f"Error saving data: {e}"


def load_from_file(filename=DATA_FILE):
    if not os.path.exists(filename):
        return [], f"File '{filename}' not found. Starting fresh."

    try:
        with open(filename, "r") as f:
            content = f.read().strip()

        if not content:
            return [], f"File '{filename}' is empty."

        data = json.loads(content)

        if not isinstance(data, list):
            return [], "File format looks wrong, expected a list of records."

        return data, f"Loaded {len(data)} record(s) from '{filename}'."

    except json.JSONDecodeError:
        return [], f"Could not read '{filename}', file may be corrupted."
    except PermissionError:
        return [], f"Cannot read '{filename}', permission denied."
    except Exception as e:
        return [], f"Error loading data: {e}"
