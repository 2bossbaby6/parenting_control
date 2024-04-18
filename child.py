import socket
import json
import time
from tcp_by_size import send_with_size, recv_by_size

child_name = "idan"
child_id = "1"
class Child:
    def __init__(self):
        self.child_name = child_name
        self.child_id = child_id
        self.server_socket = socket.socket()
        self.server_socket.connect(("127.0.0.1", 33445))
        self.connected_to_server = False

    def login_to_server(self):
        # Implement server connection logic
        data = "CHILDINSKID|" + self.child_name + "|" + self.child_id
        send_with_size(self.server_socket, data.encode())
        data = recv_by_size(self.server_socket)
        print(data.decode())

    def create_user(self):
        # Implement child registration on the server logic
        pass

    def receive_parental_control_commands(self):
        # Implement receiving commands from the parent logic
        pass

    def show_popup_message(self, message):
        # Implement showing popup message logic
        pass

    def show_usage_limit_screen(self):
        # Implement showing usage limit screen logic
        pass

    def notify_parent_restricted_access_attempt(self, website):
        # Implement notifying parent of restricted access attempt logic
        pass


# Example Usage:
child_name = input("Enter your name: ")
child = Child(child_name)
child.connect_to_server()

if not child.connected_to_server:
    print("Failed to connect to the server. Exiting.")
    exit()

child.register_on_server()
child.run_background_monitoring()



