"""
manager.py
----------
Defines the StudentManager class which controls the full collection of
student records, coordinates all operations, and delegates file I/O.
"""

from student import Student
from file_handler import save_to_file, load_from_file, DATA_FILE
from calculations import get_class_statistics


class StudentManager:
    """
    Manages the list of Student objects.
    Provides add, view, search, update, delete, statistics, save, and load.
    """

    def __init__(self):
        self.students = []         # list – ordered collection of Student objects
        self.student_ids = set()   # set – fast duplicate-ID detection

    # ── Add ───────────────────────────────────────────────────────────────────

    def add_student(self, student_id, name, marks):
        """
        Create and store a new Student.
        Returns (True, message) on success or (False, error) on failure.
        """
        if not student_id or not name:
            return False, "Student ID and name cannot be empty."

        if student_id in self.student_ids:
            return False, f"Student ID '{student_id}' already exists."

        student = Student(student_id, name, marks)
        self.students.append(student)
        self.student_ids.add(student_id)
        return True, f"Student '{name}' (ID: {student_id}) added successfully."

    # ── View ──────────────────────────────────────────────────────────────────

    def get_all_students(self):
        """Return the full list of Student objects."""
        return self.students

    # ── Search ────────────────────────────────────────────────────────────────

    def search_student(self, query):
        """
        Search by student ID (exact) or by name (case-insensitive substring).
        Returns a list of matching Student objects (may be empty).
        """
        query = query.strip().lower()
        results = []
        for student in self.students:
            id_match   = student.student_id.lower() == query
            name_match = query in student.name.lower()
            if id_match or name_match:
                results.append(student)
        return results

    def find_by_id(self, student_id):
        """Return the Student with the given ID, or None if not found."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    # ── Update ────────────────────────────────────────────────────────────────

    def update_student(self, student_id, new_name=None, new_marks=None):
        """
        Update the name and/or marks for a student identified by ID.
        Returns (True, message) or (False, error).
        """
        student = self.find_by_id(student_id)
        if student is None:
            return False, f"Student ID '{student_id}' not found."

        if new_name is not None and new_name.strip():
            student.name = new_name.strip()

        if new_marks is not None:
            student.marks = new_marks
            student.calculate_results()  # recalculate after mark change

        return True, f"Student '{student_id}' updated successfully."

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_student(self, student_id):
        """
        Remove a student from the list and the ID set.
        Returns (True, message) or (False, error).
        """
        for index, student in enumerate(self.students):
            if student.student_id == student_id:
                removed_name = student.name
                self.students.pop(index)
                self.student_ids.discard(student_id)
                return True, f"Student '{removed_name}' (ID: {student_id}) deleted."
        return False, f"Student ID '{student_id}' not found."

    # ── Statistics ────────────────────────────────────────────────────────────

    def get_statistics(self):
        """
        Compute class-level statistics using NumPy (via calculations module).
        Returns (stats_dict, message) or (None, error_message).
        """
        if not self.students:
            return None, "No student records available for statistics."

        percentages = [s.percentage for s in self.students]
        stats = get_class_statistics(percentages)
        return stats, "Statistics calculated successfully."

    def get_top_students(self, n=3):
        """Return the top N students sorted by percentage (descending)."""
        sorted_students = sorted(
            self.students, key=lambda s: s.percentage, reverse=True
        )
        return sorted_students[:n]

    def get_failed_students(self):
        """Return a list of students who failed."""
        return [s for s in self.students if s.status == "Fail"]

    # ── File operations ───────────────────────────────────────────────────────

    def save_data(self, filename=DATA_FILE):
        """Save all records to a JSON file."""
        return save_to_file(self.students, filename)

    def load_data(self, filename=DATA_FILE):
        """
        Load records from a JSON file and rebuild the students list.
        Returns a status message string.
        """
        raw_records, message = load_from_file(filename)

        if raw_records:
            self.students = []
            self.student_ids = set()
            skipped = 0
            for record in raw_records:
                try:
                    student = Student.from_dict(record)
                    if student.student_id in self.student_ids:
                        skipped += 1
                        continue
                    self.students.append(student)
                    self.student_ids.add(student.student_id)
                except (KeyError, TypeError, ValueError):
                    skipped += 1  # skip corrupted individual records

            if skipped:
                message += f" ({skipped} corrupted record(s) skipped.)"

        return message
