import socket
import tkinter as tk
from tkinter import CENTER

def receive_message():
    message = conn.recv(1024).decode()
    message_label.configure(text=message)

def on_closing():
    root.withdraw()  # Hide the window instead of closing it

# Create a TCP/IP socket
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('localhost', 12345))

# GUI setup
root = tk.Tk()
root.title("Client")

# Set window size and position
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width - window_width) / 2)
y_coordinate = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Message label with larger font size
message_label = tk.Label(root, text="", wraplength=380, font=("Arial", 14))
message_label.pack(pady=20)

# Start listening for messages
receive_message()

# Bind the closing event to on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()