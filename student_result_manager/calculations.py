"""
calculations.py
---------------
All numeric calculations using NumPy.
Also holds the constants (tuples) shared across the project.
"""

import numpy as np

# ── Constants stored as tuples ────────────────────────────────────────────────

SUBJECTS = (
    "Mathematics",
    "English",
    "Physics",
    "Chemistry",
    "Computer Science",
)

# (minimum percentage, grade label)
GRADE_BANDS = (
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
)

MAX_MARK = 100          # maximum mark per subject
PASS_PERCENTAGE = 50.0  # minimum percentage to pass


# ── Per-student calculations ──────────────────────────────────────────────────

def calculate_total(marks_list):
    """Return the sum of all marks."""
    return int(np.sum(marks_list))


def calculate_percentage(total, num_subjects):
    """Return percentage based on total marks and number of subjects."""
    max_total = num_subjects * MAX_MARK
    if max_total == 0:
        return 0.0
    return round((total / max_total) * 100, 2)


def get_grade(percentage):
    """Return the letter grade for a given percentage."""
    for threshold, grade in GRADE_BANDS:
        if percentage >= threshold:
            return grade
    return "F"


def get_status(percentage):
    """Return Pass or Fail."""
    return "Pass" if percentage >= PASS_PERCENTAGE else "Fail"


# ── Per-subject statistics for one student ────────────────────────────────────

def subject_average(marks_list):
    """Return the mean mark across subjects for one student."""
    return round(float(np.mean(marks_list)), 2)


def subject_max(marks_list):
    """Return the highest mark among subjects for one student."""
    return int(np.max(marks_list))


def subject_min(marks_list):
    """Return the lowest mark among subjects for one student."""
    return int(np.min(marks_list))


# ── Class-level statistics (across all students) ──────────────────────────────

def get_class_statistics(all_percentages):
    """
    Accept a list of student percentages and return a dictionary with
    class-level statistics computed by NumPy.
    """
    arr = np.array(all_percentages, dtype=float)
    pass_mask = arr >= PASS_PERCENTAGE

    return {
        "class_average":  round(float(np.mean(arr)), 2),
        "highest":        round(float(np.max(arr)), 2),
        "lowest":         round(float(np.min(arr)), 2),
        "median":         round(float(np.median(arr)), 2),
        "std_deviation":  round(float(np.std(arr)), 2),
        "pass_count":     int(np.sum(pass_mask)),
        "fail_count":     int(np.sum(~pass_mask)),
        "total_students": len(all_percentages),
    }
