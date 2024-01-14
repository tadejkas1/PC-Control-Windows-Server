from flask import Flask, request, render_template
import subprocess
import psutil
import os
import time
import ctypes
import win32api, win32con
import wmi

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
    return render_template("suscess.html")

@app.route('/monitor-off', methods=['GET', 'POST'])
def off():
    try:
        subprocess.Popen(['D:/Programs/NirSoft/nircmd.exe', 'monitor', 'off'])
        print(workstation_locked)
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
    return render_template("suscess.html")  # Corrected the typo here

@app.route('/sleep', methods=['GET', 'POST'])
def sleep_pc():
    try:
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        return render_template("suscess.html")
        print(workstation_locked)
    except Exception as e:
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
        current_process.terminate()  # Terminate the process

@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90)
