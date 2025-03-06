import tkinter as tk
import os
from tkinter import filedialog

def on_button_click():
    initial_dir = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    print("Selected file:", file_path)
    # Open the file here and do something with it

root = tk.Tk()

button = tk.Button(root, text="Select file", command=on_button_click)
button.pack()

root.mainloop()

