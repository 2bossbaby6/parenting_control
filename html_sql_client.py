import tkinter as tk
import socket
from tcp_by_size import send_with_size, recv_by_size
from zlib import decompress
from socket import socket as socki
import pygame

WIDTH = 1000
HEIGHT = 700


class CommandClient:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.connect(("127.0.0.1", 33445))
        self.children = {}
        self.current_child = ""
        self.create_commands = [{"label": "Create new customer", "action": "PARENINSPAR", "inputs": ["name", "password", "email", "address", "phone"]}]
        self.commands = [
            {"label": "Time manager", "action": "PARENTMNAGE", "inputs": [""]},
            {"label": "Set timer for a break", "action": "PARENABREAK", "inputs": ["section time", "break time"]},
            {"label": "Create new child account", "action": "PARENINSKID", "inputs": ["child name", "parent name", "parent id", "birthday date"]},
            {"label": "Website blocking", "action": "PARENDLTUSR", "inputs": ["website address"]},
            {"label": "Send a message to your kid", "action": "PARENMESSAG", "inputs": ["message"]},
            {"label": "Share screen", "action": "SHARESCREEN", "inputs": []},
            {"label": "Exit", "action": "PARENRULIVE", "inputs": []}
        ]

    def execute_command(self, command_data, input_entries, result_label):
        action = command_data["action"]
        if action == "SHARESCREEN":
            self.share_screen()
        else:
            inputs = input_entries
            data = action + self.children[self.current_child]

            for input_entry in inputs:
                data += "|" + input_entry.get()

            send_with_size(self.server_socket, data.encode())
            response = recv_by_size(self.server_socket).decode()
            response = response[7:]
            result_label.config(text="Output:\n" + response)

    def create_command_window(self, command_data):
        command_window = tk.Toplevel(self.root)
        command_window.title(command_data["label"])

        input_entries = []
        for input_label in command_data["inputs"]:
            tk.Label(command_window, text=input_label + ":").pack()
            entry = tk.Entry(command_window)
            entry.pack()
            input_entries.append(entry)

        result_label = tk.Label(command_window, text="Output:")
        result_label.pack()

        submit_button = tk.Button(command_window, text="Submit",
                                  command=lambda: self.execute_command(command_data, input_entries, result_label))
        submit_button.pack()

    def create_user_window(self):
        user_window = tk.Toplevel()
        user_window.title("Create User")

        input_entries = []
        for input_label in self.create_commands[0]["inputs"]:
            tk.Label(user_window, text=input_label + ":").pack()
            entry = tk.Entry(user_window)
            entry.pack()
            input_entries.append(entry)

        result_label = tk.Label(user_window, text="Output:")
        result_label.pack()

        submit_button = tk.Button(user_window, text="Create", command=lambda: self.create_new_user(input_entries, result_label))
        submit_button.pack()

    def create_new_user(self, input_entries, result_label):
        user_name = input_entries[0].get()

        if "--" in user_name:
            result_label.config(text="Invalid name, names cannot contain '--'")
            return

        self.execute_command(self.create_commands[0], input_entries, result_label)

    def handle_login(self):
        name = self.name_entry.get()
        password = self.password_entry.get()
        user_id = self.id_entry.get()

        if "--" in name:
            response = "no"
        else:
            login_data = f"PARENLOGINN|{name}|{password}|{user_id}"
            send_with_size(self.server_socket, login_data.encode())
            response = recv_by_size(self.server_socket).decode()
            response = response[8:]

        if response == "yes":
            self.login_window.destroy()
            self.create_child_selection_window()
        else:
            self.login_error_label.config(text="Invalid login, please try again")

    def create_child_selection_window(self):
        self.master = tk.Tk()
        self.master.title("Select Child")

        self.names = []

        send_with_size(self.server_socket, "PARENGETKID")
        children = recv_by_size(self.server_socket).decode()
        children = children[1:-1]
        children = children.split(",")

        for child in children:
            child = child[1:-1]
            self.children[child[1:]] = child[0]
            child = child[1:]
            self.names.append(child)

        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(pady=10)

        for name in self.names:
            self.listbox.insert(tk.END, name)

        self.select_button = tk.Button(self.master, text="Select", command=self.print_selection)
        self.select_button.pack()

        self.master.mainloop()

    def print_selection(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_name = self.listbox.get(index)
            self.current_child = selected_name
            print(self.current_child)
            self.open_main_window(selected_name)

    def open_main_window(self, selected_child_name):
        self.master.destroy()
        self.create_main_window(selected_child_name)

    def create_main_window(self, selected_child_name):
        self.root = tk.Tk()
        self.root.title("Commands")

        for command_data in self.commands:
            tk.Button(self.root, text=command_data["label"], command=lambda cmd=command_data: self.create_command_window(cmd)).pack()

        print("Selected Child:", selected_child_name)

        self.root.mainloop()

    def recvall(self, conn, length):
        """ Retreive all pixels. """

        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))
            if not data:
                return data
            buf += data
        return buf

    def share_screen(self, host='192.168.68.117', port=5000):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        watching = True

        sock = socki()
        sock.connect((host, port))
        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break

                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(sock.recv(1), byteorder='big')
                size = int.from_bytes(sock.recv(size_len), byteorder='big')
                pixels = decompress(self.recvall(sock, size))

                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                # Display the picture
                screen.blit(img, (200, 100))
                pygame.display.flip()
                clock.tick(60)
        finally:
            sock.close()
            pygame.quit()  # Properly quit Pygame when exiting the screen sharing

    def run(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")

        tk.Label(self.login_window, text="Name:").pack()
        self.name_entry = tk.Entry(self.login_window)
        self.name_entry.pack()

        tk.Label(self.login_window, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        tk.Label(self.login_window, text="ID:").pack()
        self.id_entry = tk.Entry(self.login_window)
        self.id_entry.pack()

        login_button = tk.Button(self.login_window, text="Login", command=self.handle_login)
        login_button.pack()

        create_user_button = tk.Button(self.login_window, text="Create User", command=self.create_user_window)
        create_user_button.pack()

        self.login_error_label = tk.Label(self.login_window, text="")
        self.login_error_label.pack()

        self.login_window.mainloop()


def login():
    client = CommandClient()
    client.run()


if __name__ == '__main__':
    login()
