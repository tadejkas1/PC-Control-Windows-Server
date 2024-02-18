from flask import Flask, request, render_template, send_from_directory, jsonify
import subprocess
import psutil
import os
import time
import ctypes
import win32api, win32con
import wmi
import logging
from logging.handlers import RotatingFileHandler
from ansi2html import Ansi2HTMLConverter

# Initialize last_log_position as a global variable
last_log_position = 0

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a rotating file handler for the logs
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO and 'HTTP' not in record.getMessage()

info_filter = InfoFilter()

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
handler.addFilter(info_filter)
logging.getLogger().addHandler(handler)

# Create an ANSI to HTML converter
ansi2html = Ansi2HTMLConverter()

"""                     PORT CONFIGURATION                     """
PORT= 90

current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
print(current_dir)

app = Flask(__name__, template_folder=current_dir, static_folder='static')

# Initialize global variables
workstation_locked = False
user = None

def get_logged_in_user():
    try:
        c = wmi.WMI()
        for user in c.Win32_ComputerSystem():
            return user.UserName
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

user = get_logged_in_user()

def lock_workstation_callback():
    global workstation_locked
    workstation_locked = True
    print("Workstation is locked.")
    print(workstation_locked)

def unlock_workstation_callback():
    global workstation_locked
    workstation_locked = False
    print("Workstation is unlocked.")
    print(workstation_locked)

@app.route('/get-lock-status')
def get_lock_status():
    return {'locked': workstation_locked}

@app.route("/", methods=['GET', 'POST'])
def admin():
    print(workstation_locked)
    return render_template("home.html", user=user, pc_locked=workstation_locked)

@app.route('/lock', methods=['GET', 'POST'])
def lock_pc():
    subprocess.call('rundll32.exe user32.dll,LockWorkStation', shell=True)
    lock_workstation_callback()
    print(workstation_locked)
    logging.info("Workstation locked successfully.")
    return render_template("suscess.html")

@app.route('/log')
def display_logs():
    with open('app.log', 'r') as log_file:
        logs = log_file.readlines()
        info_logs = [log for log in logs if 'INFO' in log and 'HTTP' not in log]
        logs_html = ansi2html.convert(''.join(info_logs))  # Convert ANSI color codes to HTML
    return render_template("logs.html", logs_html=logs_html)

@app.route('/get-logs')
def get_logs():
    global last_log_position

    with open('app.log', 'r') as log_file:
        # Move to the last known position in the log file
        log_file.seek(last_log_position)
        # Read new logs
        new_logs = log_file.read()
        # Update the last known position
        last_log_position = log_file.tell()

    logs_html = ansi2html.convert(new_logs)  # Convert ANSI color codes to HTML
    return jsonify({'logs_html': logs_html})

@app.route('/monitor-off', methods=['GET', 'POST'])
def off():
    try:
        subprocess.Popen(['D:/Programs/NirSoft/nircmd.exe', 'monitor', 'off'])
        print(workstation_locked)
        logging.info("Monitor turned OFF successfully.")
        return render_template("sucsess.html")
    except Exception as e:
        print(workstation_locked)
        return render_template("off.html")

@app.route('/monitor-on', methods=['GET', 'POST'])
def on():
    win32api.keybd_event(win32con.VK_LSHIFT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_LSHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
    unlock_workstation_callback()
    print(workstation_locked)
    logging.info("Monitor turned ON successfully.")
    return render_template("suscess.html")  # Corrected the typo here

@app.route('/sleep', methods=['GET', 'POST'])
def sleep_pc():
    try:
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        logging.info("PC going to sleep successfully.")
        return render_template("suscess.html")
        print(workstation_locked)
    except Exception as e:
        logging.info("PC going to sleep successfully.")
        print(workstation_locked)
        return f"An error occurred: {e}"

@app.route('/quit', methods=['GET', 'POST'])
def quit():
    try:
        time.sleep(2)  # Wait for 2 seconds before exiting
        print(workstation_locked)
        return render_template("suscess.html")
    except Exception as e:
        print(workstation_locked)
        return f"An error occurred: {e}"
    finally:
        current_process = psutil.Process()
        print(workstation_locked)
        logging.info("Program shutting down.")
        current_process.terminate()  # Terminate the process

# Add this line to serve the favicon.ico
@app.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
