"""
main.py
-------
Entry point for the Student Result Manager & Analyzer.
Run this file to start the application:
    python main.py
"""

import tkinter as tk
from gui import ResultManagerApp


def main():
    root = tk.Tk()
    app = ResultManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
