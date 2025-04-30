import tkinter as tk
from tkinter import messagebox
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

class JudgeApp:
    def _init_(self, root):  # ✅ Fixed constructor name
        self.root = root
        self.root.title("Judge - Set the Secret Number")
        self.root.geometry("400x200")
        self.root.configure(bg="#1c1c1c")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.connected = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # UI Elements
        self.label = tk.Label(root, text="Enter Secret Number:", font=("Arial", 14), fg="white", bg="#1c1c1c")
        self.label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 16), width=10, justify='center')
        self.entry.pack()

        self.submit_btn = tk.Button(root, text="Submit", font=("Arial", 12), command=self.send_secret)
        self.submit_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="Connecting to server...", font=("Arial", 12), fg="lime", bg="#1c1c1c")
        self.status_label.pack()

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.sock.connect((HOST, PORT))
            self.connected = True
            print("Connected to server as Judge.")
            self.status_label.config(text="✅ Connected. Enter number.")
        except Exception as e:
            self.status_label.config(text="❌ Connection failed.")
            messagebox.showerror("Connection Error", str(e))
            self.root.after(2000, self.root.destroy)

    def send_secret(self):
        if not self.connected:
            return
        try:
            number = int(self.entry.get().strip())
            self.sock.sendall(str(number).encode())
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')
            self.status_label.config(text="🔒 Number sent. Waiting for guesser...")
            threading.Thread(target=self.listen_for_result, daemon=True).start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send number: {e}")
            self.on_close()

    def listen_for_result(self):
        try:
            result = self.sock.recv(1024).decode()
            self.status_label.config(text=f"🎉 {result}")
        except Exception as e:
            self.status_label.config(text="⚠ Lost connection.")
            print(f"Error receiving result: {e}")
        finally:
            self.sock.close()

    def on_close(self):
        try:
            self.sock.close()
        except:
            pass
        self.root.destroy()

if _name_ == "_main_":  # ✅ Fixed main guard
    root = tk.Tk()
    app = JudgeApp(root)
    root.mainloop()
      