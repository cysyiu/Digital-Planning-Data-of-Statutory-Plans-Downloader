import tkinter as tk
from tkinter import ttk
import subprocess

def download_data():
    selected_option = dropdown.get()

    if selected_option == 'OZP':
        subprocess.call(['python', 'OZP_SHP.py'])
    elif selected_option == 'DEV_PLAN':
        subprocess.call(['python', 'DEV_PLAN_SHP.py'])

window = tk.Tk()
window.title("Data Downloader")

label = ttk.Label(window, text="Select an option:")
label.pack()

options = ['OZP', 'DEV_PLAN']
dropdown = ttk.Combobox(window, values=options)
dropdown.pack()

dropdown.current(0)

button = ttk.Button(window, text="Download", command=download_data)
button.pack()

window.mainloop()

# Start the Tkinter event loop
window.mainloop()

# Start the application
window.mainloop()