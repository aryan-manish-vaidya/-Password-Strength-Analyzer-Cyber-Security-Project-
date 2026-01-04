import tkinter as tk
from tkinter import messagebox
from cli_version import analyze_password

def check_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Input Error", "Enter a password")
        return

    strength, entropy, feedback, years = analyze_password(pwd)

    result = f"Strength: {strength}\nEntropy: {entropy} bits\nBrute-force Time: {years:.2f} years"
    if feedback:
        result += "\n\nSuggestions:\n" + "\n".join(f"- {f}" for f in feedback)

    output.config(text=result)

root = tk.Tk()
root.title("Password Strength Analyzer")

tk.Label(root, text="Enter Password").pack(pady=5)
entry = tk.Entry(root, show="*", width=30)
entry.pack()

tk.Button(root, text="Analyze", command=check_password).pack(pady=10)
output = tk.Label(root, text="", justify="left")
output.pack(pady=10)

root.mainloop()
