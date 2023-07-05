import tkinter as tk
from tkinter import filedialog
import configparser
import subprocess


def save_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'api_key': api_key_entry.get(),
        'user_info': user_info_entry.get(),
        'webs': webs_entry.get()
    }

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    messagebox.showinfo('Success', 'Config file saved successfully.')


def choose_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(tk.END, filename)


def run_main():
    subprocess.run(['python', 'main.py', 'reg'])


# Create the main Tkinter window
root = tk.Tk()
root.title('Config App')

# Define the responsive dimensions
width = root.winfo_screenwidth() * 0.5
height = root.winfo_screenheight() * 0.5

# Set the window dimensions and position it in the center
root.geometry(f'{int(width)}x{int(height)}+{int((root.winfo_screenwidth() - width) / 2)}+{int((root.winfo_screenheight() - height) / 2)}')

# Create the API Key label and entry field
api_key_label = tk.Label(root, text='API Key:')
api_key_label.pack()

api_key_entry = tk.Entry(root)
api_key_entry.pack()

# Create the User Info label, entry field, and file chooser button
user_info_label = tk.Label(root, text='User Info:')
user_info_label.pack()

user_info_entry = tk.Entry(root)
user_info_entry.pack()

user_info_button = tk.Button(root, text='Choose File', command=lambda: choose_file(user_info_entry))
user_info_button.pack()

# Create the Webs label, entry field, and file chooser button
webs_label = tk.Label(root, text='Webs:')
webs_label.pack()

webs_entry = tk.Entry(root)
webs_entry.pack()

webs_button = tk.Button(root, text='Choose File', command=lambda: choose_file(webs_entry))
webs_button.pack()

# Create the Save button
save_button = tk.Button(root, text='Save', command=save_config)
save_button.pack()

# Create the Run button
run_button = tk.Button(root, text='Run Main', command=run_main)
run_button.pack()

# Load default values from config.ini if it exists
config = configparser.ConfigParser()
if 'config.ini' in config.read('config.ini'):
    api_key_entry.insert(tk.END, config.get('SETTINGS', 'api_key'))
    user_info_entry.insert(tk.END, config.get('SETTINGS', 'user_info'))
    webs_entry.insert(tk.END, config.get('SETTINGS', 'webs'))

# Start the Tkinter event loop
root.mainloop()
