# deep_ai_gui.py

import tkinter as tk
from tkinter import simpledialog, messagebox
import torch
import torch.nn as nn
import numpy as np

# Environment settings
LOW = 1
HIGH = 100

# Define the QNetwork (same as used in training)
class QNetwork(nn.Module):
    def _init_(self):
        super(QNetwork, self)._init_()
        self.fc1 = nn.Linear(3, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, (HIGH - LOW + 1))

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DeepAIGuesser:
    def _init_(self):
        self.low = LOW
        self.high = HIGH
        self.model = QNetwork()
        self.model.load_state_dict(torch.load("deep_ai_model.pth"))
        self.model.eval()

    def get_state(self, guess):
        return np.array([self.low / 100, self.high / 100, guess / 100], dtype=np.float32)

    def make_guess(self):
        with torch.no_grad():
            guess = np.random.randint(self.low, self.high + 1)
            state = self.get_state(guess)
            state_tensor = torch.FloatTensor(state)
            q_values = self.model(state_tensor)
            action = torch.argmax(q_values).item() + 1
            if action < self.low:
                action = self.low
            if action > self.high:
                action = self.high
            return action

    def feedback(self, result):
        if result == "low":
            self.low = max(self.low, self.current_guess + 1)
        elif result == "high":
            self.high = min(self.high, self.current_guess - 1)

class DeepAIGameGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Deep AI Guesser")
        self.root.geometry("400x250")
        self.root.configure(bg="black")

        self.secret_number = simpledialog.askinteger("Your Number", "Enter a number between 1 and 100 (AI won't see it):", minvalue=1, maxvalue=100)
        if not self.secret_number:
            self.root.destroy()
            return

        self.ai = DeepAIGuesser()

        self.label = tk.Label(root, text="Deep AI is guessing your number!", font=("Arial", 16), fg="cyan", bg="black")
        self.label.pack(pady=20)

        self.guess_label = tk.Label(root, text="", font=("Arial", 24, "bold"), fg="white", bg="black")
        self.guess_label.pack(pady=10)

        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.pack()

        self.too_low_button = tk.Button(self.button_frame, text="Too Low", command=self.too_low, width=10, font=("Arial", 12))
        self.too_low_button.grid(row=0, column=0, padx=5)

        self.correct_button = tk.Button(self.button_frame, text="Correct!", command=self.correct, width=10, font=("Arial", 12))
        self.correct_button.grid(row=0, column=1, padx=5)

        self.too_high_button = tk.Button(self.button_frame, text="Too High", command=self.too_high, width=10, font=("Arial", 12))
        self.too_high_button.grid(row=0, column=2, padx=5)

        self.next_guess()

    def next_guess(self):
        guess = self.ai.make_guess()
        self.ai.current_guess = guess
        self.guess_label.config(text=f"Is it {guess}?")

    def too_low(self):
        self.ai.feedback("low")
        self.next_guess()

    def too_high(self):
        self.ai.feedback("high")
        self.next_guess()

    def correct(self):
        messagebox.showinfo("Yay!", f"Deep AI guessed your number {self.ai.current_guess}!")
        self.root.destroy()

if _name_ == "_main_":
    root = tk.Tk()
    app = DeepAIGameGUI(root)
    root.mainloop()