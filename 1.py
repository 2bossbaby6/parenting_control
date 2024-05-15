import sqlite3
import time
import pygetwindow as gw

def record_screen_time():
    conn = sqlite3.connect('screen_time.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS ScreenTime
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 app TEXT NOT NULL, 
                 time INTEGER NOT NULL)''')

    active_apps = {}  # Dictionary to store start time of each active app

    while True:
        current_active_app = gw.getActiveWindowTitle()
        current_time = int(time.time())

        if current_active_app:
            if current_active_app not in active_apps:
                active_apps[current_active_app] = current_time
            else:
                # Calculate the screen time and update the database
                time_diff = current_time - active_apps[current_active_app]
                c.execute("INSERT INTO ScreenTime (app, time) VALUES (?, ?)", (current_active_app, time_diff))
                conn.commit()
                # Update the start time for the active app
                active_apps[current_active_app] = current_time

        time.sleep(1)  # Record every second

    conn.close()

if __name__ == "__main__":
    record_screen_time()