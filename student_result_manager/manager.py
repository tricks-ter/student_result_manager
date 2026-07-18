from student import Student
from file_handler import save_to_file, load_from_file, DATA_FILE
from calculations import get_class_statistics


class StudentManager:

    def __init__(self):
        self.students = []       # list to store all student objects
        self.student_ids = set() # set to track unique IDs

    def add_student(self, student_id, name, marks):
        if not student_id or not name:
            return False, "Student ID and name cannot be empty."

        # check for duplicate ID using the set
        if student_id in self.student_ids:
            return False, f"Student ID '{student_id}' already exists."

        student = Student(student_id, name, marks)
        self.students.append(student)
        self.student_ids.add(student_id)
        return True, f"Student '{name}' (ID: {student_id}) added successfully."

    def get_all_students(self):
        return self.students

    def search_student(self, query):
        query = query.strip().lower()
        results = []
        for student in self.students:
            if student.student_id.lower() == query or query in student.name.lower():
                results.append(student)
        return results

    def find_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_student(self, student_id, new_name=None, new_marks=None):
        student = self.find_by_id(student_id)
        if student is None:
            return False, f"Student ID '{student_id}' not found."

        if new_name is not None and new_name.strip():
            student.name = new_name.strip()

        if new_marks is not None:
            student.marks = new_marks
            student.calculate_results()

        return True, f"Student '{student_id}' updated successfully."

    def delete_student(self, student_id):
        for index, student in enumerate(self.students):
            if student.student_id == student_id:
                removed_name = student.name
                self.students.pop(index)
                self.student_ids.discard(student_id)
                return True, f"Student '{removed_name}' (ID: {student_id}) deleted."
        return False, f"Student ID '{student_id}' not found."

    def get_statistics(self):
        if not self.students:
            return None, "No student records available for statistics."

        percentages = [s.percentage for s in self.students]
        stats = get_class_statistics(percentages)
        return stats, "Statistics calculated successfully."

    def get_top_students(self, n=3):
        sorted_students = sorted(self.students, key=lambda s: s.percentage, reverse=True)
        return sorted_students[:n]

    def get_failed_students(self):
        return [s for s in self.students if s.status == "Fail"]

    def save_data(self, filename=DATA_FILE):
        return save_to_file(self.students, filename)

    def load_data(self, filename=DATA_FILE):
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
                    skipped += 1

            if skipped:
                message += f" ({skipped} bad record(s) skipped.)"

        return message
