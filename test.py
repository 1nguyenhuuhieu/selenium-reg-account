import tkinter as tk
from tkinter import filedialog
import configparser
import subprocess
import os

CONFIG_FILE = 'config.ini'

def save_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'api_key': api_key_entry.get(),
        'user_info': user_info_entry.get(),
        'webs': webs_entry.get()
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        # Create the config file if it doesn't exist
        save_config()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    api_key_entry.delete(0, tk.END)
    api_key_entry.insert(0, config['SETTINGS']['api_key'])
    user_info_entry.delete(0, tk.END)
    user_info_entry.insert(0, config['SETTINGS']['user_info'])
    webs_entry.delete(0, tk.END)
    webs_entry.insert(0, config['SETTINGS']['webs'])

def run_main_py(arg):
    subprocess.run(['python', 'main.py', arg])

def choose_user_info_file():
    filename = filedialog.askopenfilename()
    user_info_entry.delete(0, tk.END)
    user_info_entry.insert(0, filename)

def choose_webs_file():
    filename = filedialog.askopenfilename()
    webs_entry.delete(0, tk.END)
    webs_entry.insert(0, filename)

root = tk.Tk()
root.title("Auto Reg Account Web Game")

# Configure grid column and row weights
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)

# API key field
api_key_label = tk.Label(root, text="API key:")
api_key_label.grid(row=0, column=0)
api_key_entry = tk.Entry(root)
api_key_entry.grid(row=0, column=1, sticky="ew")

# User info field
user_info_label = tk.Label(root, text="User info:")
user_info_label.grid(row=1, column=0)
user_info_entry = tk.Entry(root)
user_info_entry.grid(row=1, column=1, sticky="ew")
user_info_button = tk.Button(root, text="Choose file", command=choose_user_info_file)
user_info_button.grid(row=1, column=2)

# Webs field
webs_label = tk.Label(root, text="Webs:")
webs_label.grid(row=2, column=0)
webs_entry = tk.Entry(root)
webs_entry.grid(row=2, column=1, sticky="ew")
webs_button = tk.Button(root, text="Choose file", command=choose_webs_file)
webs_button.grid(row=2, column=2)

# Save button
save_button = tk.Button(root, text="Save", command=save_config)
save_button.grid(row=3, column=0, sticky="ew")

# Load button
load_button = tk.Button(root, text="Load", command=load_config)
load_button.grid(row=3, column=1, sticky="ew")

# Reg User button
reg_button = tk.Button(root, text="Reg User", command=lambda: run_main_py('reg'))
reg_button.grid(row=4, column=0, sticky="ew")

# Add Bank button
add_bank_button = tk.Button(root, text="Add Bank", command=lambda: run_main_py('add_bank'))
add_bank_button.grid(row=4, column=1, sticky="ew")

# Load config on app start
load_config()

# Author information
author_info = tk.Label(root, text="Author: Nguyen Huu Hieu")
author_info.grid(row=5, column=0, columnspan=2, sticky="w")
email_info = tk.Label(root, text="Email: 1nguyenhuuhieu@gmail.com")
email_info.grid(row=6, column=0, columnspan=2, sticky="w")
phone_info = tk.Label(root, text="Phone/Zalo: 0946127555")
phone_info.grid(row=7, column=0, columnspan=2, sticky="w")
version_info = tk.Label(root, text="Version: 1.0    Date Created: 07/05/2023")
version_info.grid(row=8, column=0, columnspan=2, sticky="w")

root.mainloop()
