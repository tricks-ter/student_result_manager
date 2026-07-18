"""
student.py
----------
Defines the Student class — the core data model of the application.
"""

from calculations import (
    calculate_total,
    calculate_percentage,
    get_grade,
    get_status,
    SUBJECTS,
)


class Student:
    """Represents one student with their marks and computed results."""

    def __init__(self, student_id, name, marks):
        """
        Parameters
        ----------
        student_id : str
        name       : str
        marks      : dict  {subject_name: mark_value}
        """
        self.student_id = student_id
        self.name = name
        self.marks = marks        # dictionary: subject -> mark

        # Calculated fields – filled by calculate_results()
        self.total = 0
        self.percentage = 0.0
        self.grade = ""
        self.status = ""

        self.calculate_results()

    # ── Core calculation ──────────────────────────────────────────────────────

    def calculate_results(self):
        """Recalculate total, percentage, grade, and pass/fail status."""
        marks_list = list(self.marks.values())
        self.total = calculate_total(marks_list)
        self.percentage = calculate_percentage(self.total, len(marks_list))
        self.grade = get_grade(self.percentage)
        self.status = get_status(self.percentage)

    # ── Serialisation helpers ─────────────────────────────────────────────────

    def to_dict(self):
        """Convert the student object to a plain dictionary for file storage."""
        return {
            "student_id": self.student_id,
            "name":       self.name,
            "marks":      self.marks,
            "total":      self.total,
            "percentage": self.percentage,
            "grade":      self.grade,
            "status":     self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Recreate a Student object from a dictionary loaded from file.
        Raises KeyError or TypeError if required fields are missing.
        """
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            marks=data["marks"],
        )
        return student

    # ── Display helper ────────────────────────────────────────────────────────

    def get_detail_lines(self):
        """Return a list of strings suitable for display in the GUI."""
        lines = [
            f"Student ID : {self.student_id}",
            f"Name       : {self.name}",
            "─" * 30,
        ]
        for subject in SUBJECTS:
            mark = self.marks.get(subject, 0)
            lines.append(f"  {subject:<22}: {mark}")
        lines += [
            "─" * 30,
            f"Total      : {self.total} / {len(self.marks) * 100}",
            f"Percentage : {self.percentage:.2f}%",
            f"Grade      : {self.grade}",
            f"Status     : {self.status}",
        ]
        return lines

    def __str__(self):
        return (
            f"[{self.student_id}] {self.name} | "
            f"{self.percentage:.2f}% | {self.grade} | {self.status}"
        )
