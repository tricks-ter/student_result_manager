import numpy as np

# subjects are fixed so i used a tuple
SUBJECTS = (
    "Mathematics",
    "English",
    "Physics",
    "Chemistry",
    "Computer Science",
)

# grade bands stored as tuple of (min percentage, grade)
GRADE_BANDS = (
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
)

MAX_MARK = 100
PASS_PERCENTAGE = 50.0


def calculate_total(marks_list):
    return int(np.sum(marks_list))


def calculate_percentage(total, num_subjects):
    max_total = num_subjects * MAX_MARK
    if max_total == 0:
        return 0.0
    return round((total / max_total) * 100, 2)


def get_grade(percentage):
    for threshold, grade in GRADE_BANDS:
        if percentage >= threshold:
            return grade
    return "F"


def get_status(percentage):
    if percentage >= PASS_PERCENTAGE:
        return "Pass"
    return "Fail"


def subject_average(marks_list):
    return round(float(np.mean(marks_list)), 2)


def subject_max(marks_list):
    return int(np.max(marks_list))


def subject_min(marks_list):
    return int(np.min(marks_list))


def get_class_statistics(all_percentages):
    # using numpy array for all the calculations
    arr = np.array(all_percentages, dtype=float)
    pass_mask = arr >= PASS_PERCENTAGE

    stats = {
        "class_average": round(float(np.mean(arr)), 2),
        "highest": round(float(np.max(arr)), 2),
        "lowest": round(float(np.min(arr)), 2),
        "median": round(float(np.median(arr)), 2),
        "std_deviation": round(float(np.std(arr)), 2),
        "pass_count": int(np.sum(pass_mask)),
        "fail_count": int(np.sum(~pass_mask)),
        "total_students": len(all_percentages),
    }
    return stats
