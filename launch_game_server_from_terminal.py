"""File contains game server launch in separated terminal"""
import subprocess

subprocess.Popen(['gnome-terminal', '-e', 'python3 launch_game_server.py'])
