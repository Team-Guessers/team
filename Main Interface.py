import tkinter as tk
import subprocess

def start_deep_ai_game():
    subprocess.Popen(["python", "deep_ai_gui.py"])

root = tk.Tk()
root.title("Number Guessing Game - Deep AI Mode")
root.geometry("400x250")
root.configure(bg="black")

title = tk.Label(
    root,
    text="Play with Deep AI",
    font=("Arial", 20, "bold"),
    fg="cyan",
    bg="black"
)
title.pack(pady=30)

btn = tk.Button(
    root,
    text="Start Game",
    command=start_deep_ai_game,
    font=("Arial", 14),
    width=20
)
btn.pack(pady=20)

root.mainloop()