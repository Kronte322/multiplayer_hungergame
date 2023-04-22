import subprocess
import time

subprocess.Popen(['gnome-terminal', '-e', 'python3 launch_lobby_for_server.py'])
time.sleep(0.1)
subprocess.Popen(['gnome-terminal', '-e', 'python3 launch_lobby_for_users.py'])
