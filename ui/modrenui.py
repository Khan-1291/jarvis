import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk

class JarvisUI:
    def __init__(self, assistant_callback):
        self.assistant_callback = assistant_callback

        # -------------------------------
        # Root window
        # -------------------------------
        self.root = tk.Tk()
        self.root.title("Jarvis AI")
        self.root.geometry("700x800")
        self.root.configure(bg="#1E1E2F")  # dark background
        self.root.resizable(False, False)

        # -------------------------------
        # Top assistant image
        # -------------------------------
        self.face_frame = tk.Frame(self.root, bg="#1E1E2F")
        self.face_frame.pack(pady=10)

        face_img = Image.open("assets/face.png").resize((120, 120))
        self.face_photo = ImageTk.PhotoImage(face_img)
        self.face_label = tk.Label(self.face_frame, image=self.face_photo, bg="#1E1E2F")
        self.face_label.pack()

        # -------------------------------
        # Chat display
        # -------------------------------
        self.chat_frame = tk.Frame(self.root, bg="#1E1E2F")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.chat_canvas = tk.Canvas(self.chat_frame, bg="#1E1E2F", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_content = tk.Frame(self.chat_canvas, bg="#1E1E2F")

        self.chat_content.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        self.chat_canvas.create_window((0, 0), window=self.chat_content, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # -------------------------------
        # Bottom input
        # -------------------------------
        self.bottom_frame = tk.Frame(self.root, bg="#1E1E2F")
        self.bottom_frame.pack(padx=10, pady=10, fill=tk.X)

        self.entry = ttk.Entry(self.bottom_frame, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill=tk.X, expand=True, padx=(0,10))
        self.entry.bind("<Return>", self.send_command)

        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_command)
        self.send_button.pack(side="left")

        # -------------------------------
        # Style
        # -------------------------------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=5)
        style.configure("TEntry", font=("Segoe UI", 11))

    # -------------------------------
    # Add chat bubble
    # -------------------------------
    def add_message(self, sender, message):
        bubble_color = "#3E8EDE" if sender == "Jarvis" else "#555555"
        fg_color = "white"

        msg_frame = tk.Frame(self.chat_content, bg="#1E1E2F", pady=5)
        msg_frame.pack(anchor="w" if sender != "Jarvis" else "e", fill=tk.X, padx=10)

        bubble = tk.Label(
            msg_frame, 
            text=message, 
            bg=bubble_color, 
            fg=fg_color, 
            wraplength=400, 
            justify="left", 
            font=("Segoe UI", 11), 
            padx=10, pady=5
        )
        bubble.pack(anchor="w" if sender != "Jarvis" else "e")

        # Auto-scroll
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    # -------------------------------
    # Send command from entry
    # -------------------------------
    def send_command(self, event=None):
        user_input = self.entry.get().strip()
        if user_input == "":
            return
        self.add_message("You", user_input)
        self.entry.delete(0, tk.END)
        response = self.assistant_callback(user_input)
        self.add_message("Jarvis", response)

    # -------------------------------
    # Run Tkinter mainloop
    # -------------------------------
    def run(self):
        self.root.mainloop()
