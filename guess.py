import tkinter as tk
from tkinter import messagebox
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

class GuesserApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Guesser - Guess the Number")
        self.root.geometry("400x250")
        self.root.configure(bg="#1c1c1c")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)  # 10 seconds timeout for connecting
        self.connected = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # UI Elements
        self.title_label = tk.Label(root, text="Guess the Secret Number", font=("Arial", 16, "bold"), fg="#00ffcc", bg="#1c1c1c")
        self.title_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 18), width=10, justify='center')
        self.entry.pack(pady=10)

        self.submit_btn = tk.Button(root, text="Guess", font=("Arial", 12), command=self.send_guess)
        self.submit_btn.pack()

        self.feedback_label = tk.Label(root, text="Connecting to server...", font=("Arial", 14), fg="orange", bg="#1c1c1c")
        self.feedback_label.pack(pady=20)

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.sock.connect((HOST, PORT))
            self.connected = True
            self.feedback_label.config(text="✅ Connected. Start guessing!")
        except Exception as e:
            self.feedback_label.config(text="❌ Connection failed.")
            messagebox.showerror("Connection Error", f"Failed to connect to server:\n{e}")
            self.root.after(2000, self.root.destroy)

    def send_guess(self):
        if not self.connected:
            messagebox.showwarning("Not connected", "You're not connected to the server.")
            return

        guess = self.entry.get().strip()
        if not guess:
            return

        try:
            int(guess)
            self.sock.sendall(guess.encode())
            self.entry.delete(0, tk.END)
            self.submit_btn.config(state='disabled')  # Disable to prevent spam
            threading.Thread(target=self.receive_feedback, daemon=True).start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send guess: {e}")
            self.on_close()

    def receive_feedback(self):
        try:
            feedback = self.sock.recv(1024).decode()
            self.feedback_label.config(text=f"📝 {feedback}")
            if "Correct" in feedback:
                self.entry.config(state='disabled')
                self.submit_btn.config(state='disabled')
            else:
                self.submit_btn.config(state='normal')  # Enable for another guess
        except Exception as e:
            self.feedback_label.config(text="⚠ Connection lost.")
            messagebox.showerror("Error", f"Error receiving feedback:\n{e}")
            self.on_close()

    def on_close(self):
        try:
            self.sock.close()
        except:
            pass
        self.root.destroy()

if _name_ == "_main_":
    root = tk.Tk()
    app = GuesserApp(root)
    root.mainloop()