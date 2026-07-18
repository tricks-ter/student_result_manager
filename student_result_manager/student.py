from calculations import calculate_total, calculate_percentage, get_grade, get_status, SUBJECTS


class Student:

    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks  # dictionary with subject names as keys

        self.total = 0
        self.percentage = 0.0
        self.grade = ""
        self.status = ""

        self.calculate_results()

    def calculate_results(self):
        marks_list = list(self.marks.values())
        self.total = calculate_total(marks_list)
        self.percentage = calculate_percentage(self.total, len(marks_list))
        self.grade = get_grade(self.percentage)
        self.status = get_status(self.percentage)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "marks": self.marks,
            "total": self.total,
            "percentage": self.percentage,
            "grade": self.grade,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["student_id"], data["name"], data["marks"])
        return student

    def get_detail_lines(self):
        lines = [
            f"Student ID : {self.student_id}",
            f"Name       : {self.name}",
            "-" * 30,
        ]
        for subject in SUBJECTS:
            mark = self.marks.get(subject, 0)
            lines.append(f"  {subject:<22}: {mark}")
        lines.append("-" * 30)
        lines.append(f"Total      : {self.total} / {len(self.marks) * 100}")
        lines.append(f"Percentage : {self.percentage:.2f}%")
        lines.append(f"Grade      : {self.grade}")
        lines.append(f"Status     : {self.status}")
        return lines

    def __str__(self):
        return f"[{self.student_id}] {self.name} | {self.percentage:.2f}% | {self.grade} | {self.status}"
