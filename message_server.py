import socket
import tkinter as tk

def send_message():
    message = entry.get()
    conn.send(message.encode())
    entry.delete(0, tk.END)

def close_connection():
    conn.close()
    server_socket.close()
    root.destroy()

def accept_connection():
    global conn
    conn, addr = server_socket.accept()
    label.configure(text=f"Connected to: {addr}")

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

# GUI setup
root = tk.Tk()
root.title("Server")
label = tk.Label(root, text="Waiting for connection...")
label.pack()
entry = tk.Entry(root)
entry.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()
close_button = tk.Button(root, text="Close Connection", command=close_connection)
close_button.pack()

# Accept connections
accept_connection()

# Start the GUI event loop
root.mainloop()