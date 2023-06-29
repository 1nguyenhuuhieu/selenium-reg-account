import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import configparser
import subprocess

class AppConfigApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Tool Auto Reg Account Configuration")
        self.geometry("600x300")
        self.resizable(True, True)

        self.config = configparser.ConfigParser()

        self.create_widgets()

    def create_widgets(self):
        # API Key Text Field
        api_key_label = tk.Label(self, text="API Key:")
        api_key_label.pack()
        self.api_key_entry = tk.Entry(self)
        self.api_key_entry.pack()

        # User Info File Path Field
        user_info_label = tk.Label(self, text="User Info File:")
        user_info_label.pack()
        self.user_info_entry = tk.Entry(self)
        self.user_info_entry.pack()
        self.user_info_button = tk.Button(self, text="Choose File", command=self.choose_user_info_file)
        self.user_info_button.pack()

        # Webs File Path Field
        webs_label = tk.Label(self, text="Webs File:")
        webs_label.pack()
        self.webs_entry = tk.Entry(self)
        self.webs_entry.pack()
        self.webs_button = tk.Button(self, text="Choose File", command=self.choose_webs_file)
        self.webs_button.pack()

        # Save Button
        save_button = tk.Button(self, text="Save", command=self.save_config)
        save_button.pack()

        # Run Main.py Button
        run_button = tk.Button(self, text="Run main.py", command=self.run_main_py)
        run_button.pack()

    def choose_user_info_file(self):
        file_path = filedialog.askopenfilename()
        self.user_info_entry.delete(0, tk.END)
        self.user_info_entry.insert(tk.END, file_path)

    def choose_webs_file(self):
        file_path = filedialog.askopenfilename()
        self.webs_entry.delete(0, tk.END)
        self.webs_entry.insert(tk.END, file_path)

    def save_config(self):
        self.config['CONFIG'] = {
            'api_key': self.api_key_entry.get(),
            'user_info': self.user_info_entry.get(),
            'webs': self.webs_entry.get()
        }

        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)

        messagebox.showinfo("Save", "Configuration saved successfully!")

    def run_main_py(self):
        subprocess.Popen(['python', 'main.py'])


if __name__ == '__main__':
    app = AppConfigApp()
    app.mainloop()
