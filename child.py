import socket
import json
import time
from tcp_by_size import send_with_size, recv_by_size
import threading
import tkinter as tk

DEBUG = True
child_name = "idan"
child_id = "0"
class Child:
    def __init__(self, child_name, child_id):
        self.child_name = child_name
        self.child_id = child_id
        self.server_socket = socket.socket()
        self.server_socket.connect(("127.0.0.1", 33445))
        self.connected_to_server = False

    def login_to_server(self):
        data = "CHILDLOGINN|" + str(self.child_name) + "|" + str(self.child_id)
        send_with_size(self.server_socket, data.encode())
        data = recv_by_size(self.server_socket).decode()
        print(data)
        fields = data.split("|")
        if fields[1] == "yes":
            thread1 = threading.Thread(target=self.handle_child, args=())
            thread1.start()
        else:
            print("error connecting")

    def handle_child(self):
        self.a_break(20, 20)
        while True:
            data = recv_by_size(self.server_socket)
            if data == "":
                print("Error: Seens Client DC")
                break
            data = data.decode()
            action = data[:6]
            data = data[7:]
            fields = data.split("|")

            if DEBUG:
                print("Got client request " + action + " -- " + str(fields))

            if action == "ABREAK":
                session_time, break_time = fields[0], fields[1]
                self.a_break(session_time, break_time)



        pass

    def a_break(self, session_time, break_time):
        while True:
            # Session time
            print(f"Session time started. You have {session_time} seconds to use the computer freely.")
            time.sleep(session_time)

            # Break time
            print(f"Break time started. Computer will be locked for {break_time} seconds.")
            self.lock_screen(break_time)
            time.sleep(break_time)

    def lock_screen(self, break_time):
        # Create a fullscreen window that prevents user interaction
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)  # Make window stay on top

        # Remove minimize, maximize, and close buttons
        root.overrideredirect(True)

        # Label to show break time message
        label = tk.Label(root, text=f"Break Time - Computer Locked for {break_time} seconds", font=("Helvetica", 24))
        label.pack(expand=True)

        # After break_time seconds, destroy the window
        root.after(break_time * 1000, root.destroy)

        root.mainloop()

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
#
# child = Child(child_name)
# child.connect_to_server()
#
# if not child.connected_to_server:
#     print("Failed to connect to the server. Exiting.")
#     exit()
#
# child.register_on_server()
# child.run_background_monitoring()



if __name__ == '__main__':
    child_name = "idan"
    child_id = "0"
    child_instance = Child(child_name, child_id)
    child_instance.login_to_server()
