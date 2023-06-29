import tkinter as tk
from tkinter import filedialog
import subprocess

class AppRunner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Script Runner")

        self.create_widgets()

    def create_widgets(self):
        self.label1 = tk.Label(self.root, text="Select a Python script:")
        self.label1.pack()

        self.file_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.file_button.pack()

        self.run_button = tk.Button(self.root, text="Run Script", command=self.run_script)
        self.run_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        self.label1.config(text="Selected Script: " + file_path)
        self.script_path = file_path

    def run_script(self):
        if hasattr(self, 'script_path'):
            try:
                subprocess.Popen(['python', self.script_path])
            except FileNotFoundError:
                tk.messagebox.showerror("Error", "Python interpreter not found.")
        else:
            tk.messagebox.showerror("Error", "No script selected.")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = AppRunner()
    app.run()
