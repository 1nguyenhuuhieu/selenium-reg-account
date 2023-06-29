import tkinter as tk
from tkinter import messagebox, filedialog
import configparser
import subprocess

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration App")
        self.geometry("300x500")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Text Input
        self.text_label = tk.Label(self, text="Text Input:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self)
        self.text_entry.pack()
        
        # Boolean Input
        self.bool_var = tk.BooleanVar()
        self.bool_check = tk.Checkbutton(self, text="Boolean Input", variable=self.bool_var)
        self.bool_check.pack()
        
        # Select Input
        self.select_label = tk.Label(self, text="Select Input:")
        self.select_label.pack()
        self.select_var = tk.StringVar()
        self.select_var.set("Option 1")  # Default option
        self.select_menu = tk.OptionMenu(self, self.select_var, "Option 1", "Option 2", "Option 3")
        self.select_menu.pack()
        
        # Load Config Button
        self.load_button = tk.Button(self, text="Load Config", command=self.load_config)
        self.load_button.pack()
        
        # Save Config Button
        self.save_button = tk.Button(self, text="Save Config", command=self.save_config)
        self.save_button.pack()
        
        # Run Main.py Button
        self.run_button = tk.Button(self, text="Run main.py", command=self.run_main_py)
        self.run_button.pack()
        
    def load_config(self):
        file_path = filedialog.askopenfilename(title="Select Config File", filetypes=[("Config Files", "*.ini")])
        if file_path:
            config = configparser.ConfigParser()
            config.read(file_path)
            
            try:
                text_input = config.get("Settings", "text_input")
                self.text_entry.delete(0, tk.END)
                self.text_entry.insert(tk.END, text_input)
                
                bool_input = config.getboolean("Settings", "bool_input")
                self.bool_var.set(bool_input)
                
                select_input = config.get("Settings", "select_input")
                self.select_var.set(select_input)
                
                messagebox.showinfo("Success", "Config loaded successfully.")
            except (configparser.Error, KeyError) as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
        
    def save_config(self):
        file_path = filedialog.asksaveasfilename(title="Save Config File", defaultextension=".ini",
                                                 filetypes=[("Config Files", "*.ini")])
        if file_path:
            config = configparser.ConfigParser()
            config["Settings"] = {
                "text_input": self.text_entry.get(),
                "bool_input": str(self.bool_var.get()),
                "select_input": self.select_var.get()
            }
            
            try:
                with open(file_path, "w") as config_file:
                    config.write(config_file)
                    
                messagebox.showinfo("Success", "Config saved successfully.")
            except (configparser.Error, IOError) as e:
                messagebox.showerror("Error", f"Failed to save config: {str(e)}")
        
    def run_main_py(self):
        subprocess.Popen(["python", "main.py"])  # Replace "main.py" with your actual file name
        
app = App()
app.mainloop()
