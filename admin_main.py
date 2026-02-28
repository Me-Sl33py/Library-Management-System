import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
import os


class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ── Window setup ──────────────────────────────────────────────
        self.title("Admin Panel")
        self.geometry("500x400")
        self.configure(bg="#1e1e2e")
        self.resizable(False, False)

        # ── Store image references HERE so they are never garbage-collected ──
        # This is the most common cause of "all icons look the same" bug.
        self.icons = {}

        self._build_ui()

    # ─────────────────────────────────────────────────────────────────
    def _load_icon(self, name: str, path: str, size=(40, 40)) -> ImageTk.PhotoImage | None:
        """
        Load an icon from disk and keep a reference inside self.icons.
        Returns None if the file doesn't exist (shows text-only button instead).
        """
        if not os.path.exists(path):
            print(f"[warn] icon not found: {path}")
            return None

        img = Image.open(path).resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.icons[name] = photo   # ← KEY: store reference to prevent GC
        return photo

    # ─────────────────────────────────────────────────────────────────
    def _make_icon_button(self, parent, label: str, icon_name: str,
                          icon_path: str, command):
        """
        Create one icon button.  Always assigns btn.image so Tkinter keeps
        the reference even if self.icons were to be cleared.
        """
        photo = self._load_icon(icon_name, icon_path)

        btn = tk.Button(
            parent,
            text=label,
            image=photo,          # may be None → shows text only
            compound=tk.TOP,      # icon above text
            command=command,
            bg="#313244",
            fg="#cdd6f4",
            activebackground="#45475a",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            width=110,
            height=110,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=8,
            pady=8,
        )

        # ← SECOND safety net: attach reference directly to the widget
        btn.image = photo

        return btn

    # ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ───────────────────────────────────────────────────
        header = tk.Label(
            self,
            text="🛠  Admin Panel",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Segoe UI", 18, "bold"),
            pady=16,
        )
        header.pack(fill=tk.X)

        # ── Icon frame ───────────────────────────────────────────────
        frame = tk.Frame(self, bg="#1e1e2e", pady=20)
        frame.pack()

        # ── Button definitions ────────────────────────────────────────
        # Each entry: (label, icon_name_key, icon_file_path, callback)
        # Replace the icon paths with your own .png/.ico files.
        buttons_cfg = [
            (
                "Users",
                "users",
                "icons/users.png",        # ← put your icon here
                lambda: self._on_click("Users"),
            ),
            (
                "Reports",
                "reports",
                "icons/reports.png",      # ← different icon
                lambda: self._on_click("Reports"),
            ),
            (
                "Settings",
                "settings",
                "icons/settings.png",     # ← different icon
                lambda: self._on_click("Settings"),
            ),
        ]

        # ── Create buttons in a loop — note each btn.image is set individually ──
        for col, (label, icon_name, icon_path, cmd) in enumerate(buttons_cfg):
            btn = self._make_icon_button(
                frame, label, icon_name, icon_path, cmd
            )
            btn.grid(row=0, column=col, padx=15, pady=10)

        # ── Status bar ───────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Select an action above.")
        status = tk.Label(
            self,
            textvariable=self.status_var,
            bg="#181825",
            fg="#a6adc8",
            font=("Segoe UI", 10),
            anchor=tk.W,
            padx=12,
            pady=6,
        )
        status.pack(side=tk.BOTTOM, fill=tk.X)

    # ─────────────────────────────────────────────────────────────────
    def _on_click(self, section: str):
        self.status_var.set(f"✔  Opened: {section}")
        print(f"Button clicked → {section}")


# ── Entry point ───────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()