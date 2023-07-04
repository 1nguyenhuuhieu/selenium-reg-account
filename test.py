import tkinter as tk
from tkinter import messagebox

def button_clicked():
    input1_text = input1.get()
    input2_text = input2.get()
    messagebox.showinfo("Button Clicked", f"Input 1: {input1_text}\nInput 2: {input2_text}")

# Create the main Tkinter window
window = tk.Tk()
window.title("My App")

# Create the input text fields
input1 = tk.Entry(window, width=30)
input1.pack(pady=10)

input2 = tk.Entry(window, width=30)
input2.pack(pady=10)

# Create the button
button = tk.Button(window, text="Click Me", command=button_clicked)
button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
