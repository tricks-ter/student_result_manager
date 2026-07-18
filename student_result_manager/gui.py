import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from manager import StudentManager
from calculations import SUBJECTS, MAX_MARK

# color variables so i dont have to repeat hex codes everywhere
DARK_BLUE  = "#2c3e50"
MID_BLUE   = "#34495e"
GREEN      = "#27ae60"
LIGHT_GREY = "#ecf0f1"
WHITE      = "#ffffff"
RED        = "#e74c3c"
ORANGE     = "#f39c12"
BLUE       = "#2980b9"
TEAL       = "#16a085"
PURPLE     = "#8e44ad"


def _labelled_entry(parent, label_text, row, default=""):
    tk.Label(parent, text=label_text, anchor=tk.W, bg=WHITE).grid(
        row=row, column=0, sticky=tk.W, padx=8, pady=4
    )
    entry = tk.Entry(parent, width=26, relief=tk.SOLID, bd=1)
    entry.insert(0, default)
    entry.grid(row=row, column=1, padx=8, pady=4)
    return entry


def _open_student_form(parent, title, manager, existing_student=None):
    result_holder = [False]

    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("420x490")
    dialog.resizable(False, False)
    dialog.grab_set()
    dialog.configure(bg=WHITE)

    tk.Label(
        dialog, text=title, font=("Arial", 13, "bold"),
        bg=DARK_BLUE, fg=WHITE, pady=8
    ).pack(fill=tk.X)

    form_frame = tk.Frame(dialog, bg=WHITE, padx=10, pady=10)
    form_frame.pack(fill=tk.X)

    is_update = existing_student is not None
    id_default   = existing_student.student_id if is_update else ""
    name_default = existing_student.name if is_update else ""

    id_entry   = _labelled_entry(form_frame, "Student ID :", 0, id_default)
    name_entry = _labelled_entry(form_frame, "Full Name  :", 1, name_default)

    if is_update:
        id_entry.config(state="disabled")

    tk.Label(
        form_frame, text="--- Subject Marks (0 - 100) ---",
        font=("Arial", 9, "italic"), bg=WHITE, fg=MID_BLUE
    ).grid(row=2, column=0, columnspan=2, pady=(8, 2))

    mark_entries = {}
    for idx, subject in enumerate(SUBJECTS):
        default_mark = ""
        if is_update:
            default_mark = str(int(existing_student.marks.get(subject, 0)))
        entry = _labelled_entry(form_frame, f"{subject} :", idx + 3, default_mark)
        mark_entries[subject] = entry

    def _validate_and_submit():
        s_id   = id_entry.get().strip()
        s_name = name_entry.get().strip()

        if not s_id:
            messagebox.showerror("Error", "Student ID cannot be empty.", parent=dialog)
            return
        if not s_name:
            messagebox.showerror("Error", "Name cannot be empty.", parent=dialog)
            return
        if not s_name.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Name should contain letters only.", parent=dialog)
            return

        marks = {}
        for subject, entry in mark_entries.items():
            raw = entry.get().strip()
            if not raw:
                messagebox.showerror("Error", f"Please enter a mark for {subject}.", parent=dialog)
                return
            try:
                mark = float(raw)
            except ValueError:
                messagebox.showerror("Error", f"'{raw}' is not a valid number for {subject}.", parent=dialog)
                return
            if mark < 0 or mark > MAX_MARK:
                messagebox.showerror("Error", f"{subject} mark must be between 0 and {MAX_MARK}.", parent=dialog)
                return
            marks[subject] = mark

        if is_update:
            success, msg = manager.update_student(s_id, s_name, marks)
        else:
            success, msg = manager.add_student(s_id, s_name, marks)

        if success:
            messagebox.showinfo("Success", msg, parent=dialog)
            result_holder[0] = True
            dialog.destroy()
        else:
            messagebox.showerror("Error", msg, parent=dialog)

    btn_text  = "Update Student" if is_update else "Add Student"
    btn_color = ORANGE if is_update else GREEN

    tk.Button(
        dialog, text=btn_text, command=_validate_and_submit,
        bg=btn_color, fg=WHITE, font=("Arial", 10, "bold"),
        relief=tk.FLAT, padx=16, pady=6, cursor="hand2"
    ).pack(pady=14)

    parent.wait_window(dialog)
    return result_holder[0]


def _show_student_detail(parent, student):
    win = tk.Toplevel(parent)
    win.title(f"Student Detail - {student.student_id}")
    win.geometry("340x360")
    win.resizable(False, False)
    win.configure(bg=WHITE)
    win.grab_set()

    tk.Label(
        win, text="Student Detail", font=("Arial", 12, "bold"),
        bg=DARK_BLUE, fg=WHITE, pady=8
    ).pack(fill=tk.X)

    text = tk.Text(win, font=("Courier", 10), bg=LIGHT_GREY,
                   relief=tk.FLAT, padx=10, pady=10, state=tk.NORMAL)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for line in student.get_detail_lines():
        text.insert(tk.END, line + "\n")

    text.config(state=tk.DISABLED)

    tk.Button(
        win, text="Close", command=win.destroy,
        bg=MID_BLUE, fg=WHITE, font=("Arial", 9), relief=tk.FLAT
    ).pack(pady=6)


def _show_statistics_window(parent, stats, top_students, failed_students):
    win = tk.Toplevel(parent)
    win.title("Class Statistics")
    win.geometry("420x540")
    win.resizable(False, False)
    win.configure(bg=WHITE)
    win.grab_set()

    tk.Label(
        win, text="Class Statistics (NumPy)", font=("Arial", 13, "bold"),
        bg=DARK_BLUE, fg=WHITE, pady=8
    ).pack(fill=tk.X)

    frame = tk.Frame(win, bg=WHITE, padx=20, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    if stats["total_students"] > 0:
        pass_rate = round((stats["pass_count"] / stats["total_students"]) * 100, 1)
    else:
        pass_rate = 0

    stat_rows = [
        ("Total Students",  str(stats["total_students"])),
        ("Class Average",   f"{stats['class_average']} %"),
        ("Highest %",       f"{stats['highest']} %"),
        ("Lowest %",        f"{stats['lowest']} %"),
        ("Median %",        f"{stats['median']} %"),
        ("Std Deviation",   f"{stats['std_deviation']} %"),
        ("Students Passed", str(stats["pass_count"])),
        ("Students Failed", str(stats["fail_count"])),
        ("Pass Rate",       f"{pass_rate} %"),
    ]

    for r, (label, value) in enumerate(stat_rows):
        tk.Label(frame, text=label + " :", anchor=tk.W,
                 font=("Arial", 10), bg=WHITE).grid(row=r, column=0, sticky=tk.W, pady=2)
        if "Pass" in label:
            color = GREEN
        elif "Fail" in label:
            color = RED
        else:
            color = DARK_BLUE
        tk.Label(frame, text=value, anchor=tk.W,
                 font=("Arial", 10, "bold"), fg=color, bg=WHITE).grid(
            row=r, column=1, sticky=tk.W, padx=14, pady=2)

    separator = tk.Frame(win, height=1, bg=LIGHT_GREY)
    separator.pack(fill=tk.X, padx=10)

    tk.Label(
        win, text="Top 3 Students", font=("Arial", 10, "bold"),
        bg=WHITE, fg=TEAL
    ).pack(anchor=tk.W, padx=20, pady=(8, 2))

    for i, s in enumerate(top_students, 1):
        tk.Label(
            win,
            text=f"  {i}. [{s.student_id}] {s.name}  -  {s.percentage:.2f}%  |  {s.grade}",
            font=("Arial", 9), bg=WHITE, fg=DARK_BLUE, anchor=tk.W
        ).pack(anchor=tk.W, padx=20)

    tk.Label(
        win, text=f"Failed Students ({len(failed_students)})",
        font=("Arial", 10, "bold"), bg=WHITE, fg=RED
    ).pack(anchor=tk.W, padx=20, pady=(8, 2))

    if failed_students:
        for s in failed_students:
            tk.Label(
                win,
                text=f"  - [{s.student_id}] {s.name}  -  {s.percentage:.2f}%",
                font=("Arial", 9), bg=WHITE, fg=RED, anchor=tk.W
            ).pack(anchor=tk.W, padx=20)
    else:
        tk.Label(win, text="  All students passed!",
                 font=("Arial", 9), bg=WHITE, fg=GREEN, anchor=tk.W).pack(anchor=tk.W, padx=20)

    tk.Button(
        win, text="Close", command=win.destroy,
        bg=MID_BLUE, fg=WHITE, font=("Arial", 9), relief=tk.FLAT, padx=12
    ).pack(pady=12)


class ResultManagerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Manager & Analyzer")
        self.root.geometry("980x600")
        self.root.minsize(800, 500)
        self.root.configure(bg=LIGHT_GREY)

        self.manager = StudentManager()

        self._build_ui()
        self._auto_load()

    def _build_ui(self):
        self._build_header()
        self._build_body()
        self._build_status_bar()

    def _build_header(self):
        header = tk.Frame(self.root, bg=DARK_BLUE, pady=10)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Student Result Manager & Analyzer",
            font=("Arial", 17, "bold"),
            fg=WHITE, bg=DARK_BLUE
        ).pack()
        tk.Label(
            header,
            text="Manage student marks · Calculate grades · Analyse class performance",
            font=("Arial", 9), fg="#bdc3c7", bg=DARK_BLUE
        ).pack()

    def _build_body(self):
        body = tk.Frame(self.root, bg=LIGHT_GREY)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self._build_sidebar(body)
        self._build_main_panel(body)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=MID_BLUE, width=170, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="MENU", font=("Arial", 10, "bold"),
            fg=LIGHT_GREY, bg=MID_BLUE, pady=6
        ).pack()

        menu_items = (
            ("Add Student",  self._cmd_add,        GREEN),
            ("View All",     self._cmd_view_all,   BLUE),
            ("Search",       self._cmd_search,     PURPLE),
            ("Update",       self._cmd_update,     ORANGE),
            ("Delete",       self._cmd_delete,     RED),
            ("Statistics",   self._cmd_statistics, TEAL),
            ("Save Data",    self._cmd_save,       MID_BLUE),
            ("Load Data",    self._cmd_load,       MID_BLUE),
            ("Exit",         self.root.quit,       "#7f8c8d"),
        )

        for label, command, colour in menu_items:
            btn = tk.Button(
                sidebar, text=label, command=command,
                bg=colour, fg=WHITE,
                font=("Arial", 9, "bold"),
                relief=tk.FLAT, width=17,
                pady=6, cursor="hand2",
                activebackground=DARK_BLUE, activeforeground=WHITE
            )
            btn.pack(pady=3, padx=8)

        tk.Label(
            sidebar,
            text="\nTip: Double-click a\nrow to view details.\nSelect a row then\nUpdate/Delete it.",
            font=("Arial", 8), fg=LIGHT_GREY, bg=MID_BLUE, justify=tk.LEFT
        ).pack(pady=(16, 0), padx=8)

    def _build_main_panel(self, parent):
        main = tk.Frame(parent, bg=WHITE, relief=tk.FLAT, bd=1)
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        filter_bar = tk.Frame(main, bg=LIGHT_GREY, pady=5)
        filter_bar.pack(fill=tk.X, padx=10, pady=(8, 0))

        tk.Label(
            filter_bar, text="Quick Filter:", font=("Arial", 9),
            bg=LIGHT_GREY
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", self._on_filter_change)
        filter_entry = tk.Entry(
            filter_bar, textvariable=self.filter_var, width=24,
            relief=tk.SOLID, bd=1
        )
        filter_entry.pack(side=tk.LEFT, padx=4)

        tk.Button(
            filter_bar, text="Clear", command=self._clear_filter,
            bg=LIGHT_GREY, relief=tk.FLAT, font=("Arial", 8), cursor="hand2"
        ).pack(side=tk.LEFT)

        self.record_count_var = tk.StringVar(value="0 record(s)")
        tk.Label(
            filter_bar, textvariable=self.record_count_var,
            font=("Arial", 9), bg=LIGHT_GREY, fg=MID_BLUE
        ).pack(side=tk.RIGHT, padx=10)

        self._build_treeview(main)

    def _build_treeview(self, parent):
        columns = ("ID", "Name", "Maths", "Eng", "Phy", "Chem", "CS",
                   "Total", "Percentage", "Grade", "Status")

        tree_frame = tk.Frame(parent, bg=WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        style.configure("Treeview", rowheight=22, font=("Arial", 9))

        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings",
            yscrollcommand=vsb.set, xscrollcommand=hsb.set
        )
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        col_config = {
            "ID": 60, "Name": 140, "Maths": 55, "Eng": 55,
            "Phy": 55, "Chem": 55, "CS": 55, "Total": 55,
            "Percentage": 80, "Grade": 50, "Status": 60,
        }
        for col, width in col_config.items():
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_treeview(c))
            self.tree.column(col, width=width, anchor=tk.CENTER, minwidth=40)

        self.tree.tag_configure("pass_row", foreground=GREEN)
        self.tree.tag_configure("fail_row", foreground=RED)
        self.tree.tag_configure("even_row", background="#f8f9fa")

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self._on_double_click)

        self._sort_column = None
        self._sort_reverse = False

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready. Load existing data or add a new student.")
        status = tk.Label(
            self.root, textvariable=self.status_var,
            relief=tk.SUNKEN, anchor=tk.W,
            font=("Arial", 9), bg="#bdc3c7", fg=DARK_BLUE, padx=8
        )
        status.pack(fill=tk.X, side=tk.BOTTOM)

    def _refresh_treeview(self, students=None):
        if students is None:
            students = self.manager.get_all_students()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, s in enumerate(students):
            tag = "pass_row" if s.status == "Pass" else "fail_row"
            if i % 2 == 0:
                tag = (tag, "even_row")
            self.tree.insert(
                "", tk.END,
                values=(
                    s.student_id, s.name,
                    int(s.marks.get("Mathematics", 0)),
                    int(s.marks.get("English", 0)),
                    int(s.marks.get("Physics", 0)),
                    int(s.marks.get("Chemistry", 0)),
                    int(s.marks.get("Computer Science", 0)),
                    s.total,
                    f"{s.percentage:.2f}%",
                    s.grade,
                    s.status,
                ),
                tags=tag,
            )

        self.record_count_var.set(f"{len(students)} record(s)")

    def _get_selected_id(self):
        selected = self.tree.selection()
        if selected:
            return self.tree.item(selected[0], "values")[0]
        return None

    def _set_status(self, message):
        self.status_var.set(message)

    def _on_double_click(self, event):
        s_id = self._get_selected_id()
        if s_id:
            student = self.manager.find_by_id(s_id)
            if student:
                _show_student_detail(self.root, student)

    def _on_filter_change(self, *args):
        query = self.filter_var.get().strip().lower()
        if not query:
            self._refresh_treeview()
            return
        all_students = self.manager.get_all_students()
        filtered = [
            s for s in all_students
            if query in s.student_id.lower() or query in s.name.lower()
        ]
        self._refresh_treeview(filtered)

    def _clear_filter(self):
        self.filter_var.set("")
        self._refresh_treeview()

    def _sort_treeview(self, column):
        students = self.manager.get_all_students()

        col_key_map = {
            "ID":         lambda s: s.student_id,
            "Name":       lambda s: s.name,
            "Total":      lambda s: s.total,
            "Percentage": lambda s: s.percentage,
            "Grade":      lambda s: s.grade,
            "Status":     lambda s: s.status,
            "Maths":      lambda s: s.marks.get("Mathematics", 0),
            "Eng":        lambda s: s.marks.get("English", 0),
            "Phy":        lambda s: s.marks.get("Physics", 0),
            "Chem":       lambda s: s.marks.get("Chemistry", 0),
            "CS":         lambda s: s.marks.get("Computer Science", 0),
        }

        if column not in col_key_map:
            return

        if self._sort_column == column:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = column
            self._sort_reverse = False

        sorted_students = sorted(students, key=col_key_map[column], reverse=self._sort_reverse)
        self._refresh_treeview(sorted_students)

    def _auto_load(self):
        msg = self.manager.load_data()
        self._refresh_treeview()
        self._set_status(f"Startup: {msg}")

    def _cmd_add(self):
        success = _open_student_form(self.root, "Add New Student", self.manager)
        if success:
            self._refresh_treeview()
            total = len(self.manager.get_all_students())
            self._set_status(f"Student added. Total records: {total}.")

    def _cmd_view_all(self):
        self.filter_var.set("")
        self._refresh_treeview()
        count = len(self.manager.get_all_students())
        self._set_status(f"Showing all {count} student(s).")

    def _cmd_search(self):
        query = simpledialog.askstring(
            "Search Student",
            "Enter Student ID or part of name:",
            parent=self.root
        )
        if query is None:
            return
        query = query.strip()
        if not query:
            messagebox.showwarning("Search", "Please enter a search term.", parent=self.root)
            return

        results = self.manager.search_student(query)
        self._refresh_treeview(results)

        if results:
            self._set_status(f"Search '{query}': found {len(results)} record(s).")
        else:
            self._set_status(f"Search '{query}': no records found.")
            messagebox.showinfo("Search Result", f"No student found matching '{query}'.", parent=self.root)

    def _cmd_update(self):
        s_id = self._get_selected_id()
        if not s_id:
            s_id = simpledialog.askstring(
                "Update Student",
                "Enter the Student ID to update:",
                parent=self.root
            )
            if not s_id:
                return
            s_id = s_id.strip()

        student = self.manager.find_by_id(s_id)
        if student is None:
            messagebox.showerror("Not Found", f"Student ID '{s_id}' not found.", parent=self.root)
            return

        success = _open_student_form(
            self.root, f"Update Student - {s_id}", self.manager,
            existing_student=student
        )
        if success:
            self._refresh_treeview()
            self._set_status(f"Student '{s_id}' updated successfully.")

    def _cmd_delete(self):
        s_id = self._get_selected_id()
        if not s_id:
            s_id = simpledialog.askstring(
                "Delete Student",
                "Enter the Student ID to delete:",
                parent=self.root
            )
            if not s_id:
                return
            s_id = s_id.strip()

        student = self.manager.find_by_id(s_id)
        if student is None:
            messagebox.showerror("Not Found", f"Student ID '{s_id}' not found.", parent=self.root)
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student '{student.name}' (ID: {s_id})?\nThis cannot be undone.",
            parent=self.root
        )
        if not confirm:
            return

        success, msg = self.manager.delete_student(s_id)
        if success:
            self._refresh_treeview()
            self._set_status(msg)
        else:
            messagebox.showerror("Error", msg, parent=self.root)

    def _cmd_statistics(self):
        stats, msg = self.manager.get_statistics()
        if stats is None:
            messagebox.showinfo("Statistics", msg, parent=self.root)
            return

        top_students    = self.manager.get_top_students(3)
        failed_students = self.manager.get_failed_students()

        _show_statistics_window(self.root, stats, top_students, failed_students)
        self._set_status("Class statistics displayed.")

    def _cmd_save(self):
        success, msg = self.manager.save_data()
        if success:
            messagebox.showinfo("Save", msg, parent=self.root)
        else:
            messagebox.showerror("Save Error", msg, parent=self.root)
        self._set_status(msg)

    def _cmd_load(self):
        confirm = messagebox.askyesno(
            "Load Data",
            "Loading will replace current records with saved data.\nContinue?",
            parent=self.root
        )
        if not confirm:
            return
        msg = self.manager.load_data()
        self._refresh_treeview()
        messagebox.showinfo("Load", msg, parent=self.root)
        self._set_status(msg)
