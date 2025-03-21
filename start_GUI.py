import tkinter as tk
from PIL import Image, ImageTk  # Requires Pillow

def show_start_gui():
    """Blocks execution until Start is clicked."""
    user_started = {'value': False}
    def on_start():
        user_started['value'] = True
        root.destroy()  # Close the GUI window

    root = tk.Tk()
    root.title("Dig It Bot!")
    root.geometry("700x850")
    root.resizable(False, False)

    container = tk.Frame(root, padx=20, pady=20)
    container.pack(fill="both", expand=True)

    # Title
    title_label = tk.Label(container, text="Dig It Bot!", font=("Arial", 20, "bold"))
    title_label.pack(pady=(0, 20))

    # Subtitle
    how_to_label = tk.Label(container, text="How To Use", font=("Arial", 16, "underline"))
    how_to_label.pack(anchor="w")

    # Instructions
    instructions = [
        "1. Go to Dig it and start digging. The digging bar needs to be showing.",
        "1a. Ideally dig in a dark place.",
        "1b. Position the camera zoomed out or in a manner where the bar has a full plain dark background to reduce errors on computer vision.",
        "2. Click the 'Start' Button below.",
        "3. Drag out a snippet of the bar as shown on the picture below:",
        "4. Make sure the bot's debugging tool is working by confirming the debugging window.",
        "5. Do not move the window and do not move the mouse around or outside the clicking area.",
        "6. AFK a while.",
        "7. Press [ESC] when you are done or want to adjust any windows/mouse."
    ]

    for text in instructions:
        is_substep = text.startswith("1a.") or text.startswith("1b.")
        tk.Label(
            container,
            text=text,
            font=("Arial", 11),
            wraplength=560,
            justify="left"
        ).pack(anchor="w", pady=2, padx=(30 if is_substep else 0))

    # Load and display image
    try:
        img = Image.open("demonstration.png")
        img = img.resize((650, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        image_label = tk.Label(container, image=photo)
        image_label.image = photo  # Keep reference
        image_label.pack(pady=15)
    except Exception as e:
        tk.Label(container, text="[ Could not load demonstration.png ]", font=("Arial", 11, "italic"), fg="gray").pack(pady=15)
        print(f"Error loading image: {e}")

    # Start Button
    start_button = tk.Button(container, text="Start", font=("Arial", 18, "bold"), width=10, height=2, command=on_start)
    start_button.pack(pady=20, ipady=50)

    root.mainloop()

    return user_started['value']
