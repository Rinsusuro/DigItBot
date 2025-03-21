# start_GUI.py

import tkinter as tk

def show_start_gui():
    """Blocks execution until Start is clicked."""
    gui_done = {'ready': False}

    def on_start():
        gui_done['ready'] = True
        root.destroy()  # Close the GUI window

    root = tk.Tk()
    root.title("Start Program")
    root.geometry("100x50")

    start_button = tk.Button(root, text="Start", font=("Arial", 12), command=on_start)
    start_button.pack()

    root.mainloop()  # Blocks until root.destroy() is called
