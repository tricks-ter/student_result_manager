import tkinter as tk
from gui import ResultManagerApp


def main():
    root = tk.Tk()
    app = ResultManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
