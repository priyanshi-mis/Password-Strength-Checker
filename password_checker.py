
import tkinter as tk
from tkinter import messagebox
import re
import string
import secrets

BG = "#0B1020"
PANEL = "#151C31"
FIELD = "#202943"
PURPLE = "#8B5CF6"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#34D399"
RED = "#FB7185"
ORANGE = "#FBBF24"

COMMON_PASSWORDS = {
    "password", "password123", "12345678",
    "qwerty123", "admin123", "welcome123",
    "iloveyou", "letmein"
}

def analyze_password(password):
    checks = [
        ("At least 8 characters", len(password) >= 8),
        ("Uppercase letter (A-Z)", bool(re.search(r"[A-Z]", password))),
        ("Lowercase letter (a-z)", bool(re.search(r"[a-z]", password))),
        ("Number (0-9)", bool(re.search(r"\d", password))),
        ("Special character (!@#...)", any(c in string.punctuation for c in password)),
        ("At least 12 characters", len(password) >= 12),
    ]

    score = sum(ok for _, ok in checks[:5])
    common = password.lower() in COMMON_PASSWORDS

    if not password:
        level, color, advice = "NOT CHECKED", MUTED, "Enter a password to begin."
    elif common:
        level, color, advice = "VERY WEAK", RED, "Avoid common passwords."
    elif score <= 2:
        level, color, advice = "WEAK", RED, "Add more character types and length."
    elif score <= 3:
        level, color, advice = "FAIR", ORANGE, "Improve length and variety."
    elif score == 4:
        level, color, advice = "GOOD", "#60A5FA", "One more improvement can help."
    else:
        level, color, advice = "STRONG", GREEN, "All five basic checks passed."

    return checks, score, level, color, advice, common


def update_analysis(*args):
    password = password_var.get()
    checks, score, level, color, advice, common = analyze_password(password)

    strength_label.config(text=level, fg=color)
    advice_label.config(text=advice, fg=color)
    score_label.config(text=f"{score}/5 checks passed")

    meter.delete("all")
    width = 330
    meter.create_rectangle(0, 0, width, 8, fill=FIELD, outline="")
    fill_width = width * score / 5
    if password and common:
        fill_color = RED
    else:
        fill_color = color
    meter.create_rectangle(0, 0, fill_width, 8, fill=fill_color, outline="")

    for i, (text, passed) in enumerate(checks):
        requirement_labels[i].config(
            text=("✓  " if passed else "○  ") + text,
            fg=GREEN if passed else MUTED
        )

    if common and password:
        warning_label.config(
            text="⚠ This is a commonly used password.",
            fg=RED
        )
    else:
        warning_label.config(text="")


def toggle_password():
    password_entry.config(show="" if show_var.get() else "*")


def generate_password():
    # Generate a random password using Python's secrets module.
    chars = string.ascii_letters + string.digits + "!@#$%&*?"
    while True:
        password = "".join(secrets.choice(chars) for _ in range(18))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
        ):
            break

    password_var.set(password)
    show_var.set(True)
    toggle_password()
    password_entry.focus_set()
    password_entry.selection_range(0, tk.END)


def copy_password():
    password = password_var.get()
    if not password:
        messagebox.showinfo("Nothing to copy", "Generate or enter a password first.")
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard.")


def clear_password():
    password_var.set("")
    show_var.set(False)
    toggle_password()
    password_entry.focus_set()


root = tk.Tk()
root.title("SecureCheck | Password Analyzer")
root.geometry("560x690")
root.configure(bg=BG)
root.resizable(False, False)

password_var = tk.StringVar()
show_var = tk.BooleanVar(value=False)
password_var.trace_add("write", update_analysis)

# Header
tk.Label(
    root, text="SECURECHECK",
    font=("Segoe UI", 11, "bold"),
    bg=BG, fg=PURPLE
).pack(pady=(22, 3))

tk.Label(
    root, text="Password Security Analyzer",
    font=("Segoe UI", 22, "bold"),
    bg=BG, fg=WHITE
).pack()

tk.Label(
    root, text="Analyze strength. Improve security.",
    font=("Segoe UI", 10),
    bg=BG, fg=MUTED
).pack(pady=(5, 18))

# Main panel
panel = tk.Frame(root, bg=PANEL, padx=24, pady=20)
panel.pack(fill="x", padx=28)

tk.Label(
    panel, text="YOUR PASSWORD",
    font=("Segoe UI", 9, "bold"),
    bg=PANEL, fg=MUTED
).pack(anchor="w", pady=(0, 8))

password_entry = tk.Entry(
    panel, textvariable=password_var,
    font=("Consolas", 13),
    show="*", bg=FIELD, fg=WHITE,
    insertbackground=WHITE, relief="flat",
    bd=0
)
password_entry.pack(fill="x", ipady=11)

tk.Checkbutton(
    panel, text="Show password",
    variable=show_var, command=toggle_password,
    bg=PANEL, fg=MUTED, selectcolor=FIELD,
    activebackground=PANEL, activeforeground=WHITE,
    font=("Segoe UI", 9), relief="flat"
).pack(anchor="w", pady=(7, 12))

# Strength section
row = tk.Frame(panel, bg=PANEL)
row.pack(fill="x")

tk.Label(
    row, text="STRENGTH LEVEL",
    font=("Segoe UI", 9, "bold"),
    bg=PANEL, fg=MUTED
).pack(side="left")

strength_label = tk.Label(
    row, text="NOT CHECKED",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL, fg=MUTED
)
strength_label.pack(side="right")

meter = tk.Canvas(
    panel, width=330, height=8,
    bg=PANEL, highlightthickness=0
)
meter.pack(fill="x", pady=12)

score_label = tk.Label(
    panel, text="0/5 checks passed",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
)
score_label.pack(anchor="w")

advice_label = tk.Label(
    panel, text="Enter a password to begin.",
    font=("Segoe UI", 10),
    bg=PANEL, fg=MUTED,
    wraplength=450
)
advice_label.pack(anchor="w", pady=(8, 2))

warning_label = tk.Label(
    panel, text="",
    font=("Segoe UI", 9, "bold"),
    bg=PANEL, fg=RED
)
warning_label.pack(anchor="w", pady=(4, 0))

# Requirements
tk.Label(
    root, text="SECURITY CHECKLIST",
    font=("Segoe UI", 10, "bold"),
    bg=BG, fg=WHITE
).pack(anchor="w", padx=34, pady=(18, 8))

requirement_labels = []
for _ in range(6):
    label = tk.Label(
        root, text="○  Waiting for input...",
        font=("Segoe UI", 10),
        bg=BG, fg=MUTED
    )
    label.pack(anchor="w", padx=42, pady=2)
    requirement_labels.append(label)

# Action buttons
buttons = tk.Frame(root, bg=BG)
buttons.pack(pady=20)

tk.Button(
    buttons, text="Generate Secure Password",
    command=generate_password,
    bg=PURPLE, fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat", cursor="hand2",
    padx=12, pady=10
).grid(row=0, column=0, padx=4, pady=4)

tk.Button(
    buttons, text="Copy",
    command=copy_password,
    bg=FIELD, fg=WHITE,
    font=("Segoe UI", 10),
    relief="flat", cursor="hand2",
    padx=18, pady=10
).grid(row=0, column=1, padx=4, pady=4)

tk.Button(
    buttons, text="Clear",
    command=clear_password,
    bg=FIELD, fg=WHITE,
    font=("Segoe UI", 10),
    relief="flat", cursor="hand2",
    padx=18, pady=10
).grid(row=0, column=2, padx=4, pady=4)

tk.Label(
    root,
    text="Privacy note: Passwords are analyzed locally, not uploaded.",
    font=("Segoe UI", 8),
    bg=BG, fg=MUTED
).pack(pady=(0, 14))

update_analysis()
root.mainloop()
