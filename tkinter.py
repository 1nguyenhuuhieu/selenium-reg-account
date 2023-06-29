import tkinter as tk
from tkinter import filedialog
import configparser

class ConfigEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("Config Editor")

        # Create a ConfigParser object
        self.config = configparser.ConfigParser()

        # Create the GUI elements
        self.label = tk.Label(master, text="Config Editor")
        self.label.pack()

        self.save_button = tk.Button(master, text="Save Config", command=self.save_config)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load Config", command=self.load_config)
        self.load_button.pack()

        self.edit_button = tk.Button(master, text="Edit Config", command=self.edit_config)
        self.edit_button.pack()

    def save_config(self):
        # Prompt user to select a file path to save the config
        file_path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI Files", "*.ini")])
        
        if file_path:
            # Get the current configuration from the ConfigParser object
            config_str = self.config_to_string()

            # Save the config to the selected file
            with open(file_path, "w") as file:
                file.write(config_str)

    def load_config(self):
        # Prompt user to select a config file to load
        file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])

        if file_path:
            # Clear the current configuration
            self.config.clear()

            # Load the config from the selected file
            self.config.read(file_path)

    def edit_config(self):
        # Create a new window for editing the config
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Config")

        # Create the GUI elements for editing the config
        for section in self.config.sections():
            section_label = tk.Label(edit_window, text=f"[{section}]")
            section_label.pack()

            for option in self.config[section]:
                option_label = tk.Label(edit_window, text=f"{option}:")
                option_label.pack()

                option_entry = tk.Entry(edit_window)
                option_entry.insert(tk.END, self.config[section][option])
                option_entry.pack()

                def update_option_value(value, section, option):
                    self.config.set(section, option, value)

                option_entry.bind("<KeyRelease>", lambda event, section=section, option=option: update_option_value(option_entry.get(), section, option))

    def config_to_string(self):
        # Convert the ConfigParser object to a string
        config_str = ""
        for section in self.config.sections():
            config_str += f"[{section}]\n"
            for option in self.config[section]:
                value = self.config[section][option]
                config_str += f"{option} = {value}\n"
            config_str += "\n"
        return config_str

root = tk.Tk()
app = ConfigEditorApp(root)
root.mainloop()
