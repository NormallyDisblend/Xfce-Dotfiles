import sys
import termios
import tty
import os
import subprocess
import shutil

options = [
    "config",
    "background",
    "gtk_config",
    "panel",
    "compositor",
    "fastfetch",
    "kitty",
]

selected = [False] * len(options)
cursor_pos = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_screen()
    print("Use arrow keys to move, Enter to toggle/select, 'q' to quit\n")
    for i, opt in enumerate(["Continue"] + options):
        cursor = "→" if i == cursor_pos else " "
        if i == 0:
            print(f"{cursor} {opt}")
        else:
            checked = "[X]" if selected[i-1] else "[ ]"
            print(f"{cursor} {checked} {opt}")

def read_key():
    if not sys.stdin.isatty():
        print("Error: Not running in a terminal. Please run this script in a terminal.")
        sys.exit(1)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def create_picom_autostart():
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    picom_desktop_path = os.path.join(autostart_dir, "picom.desktop")
    content = """[Desktop Entry]
Type=Application
Name=Picom
Exec=picom --config ~/.config/picom.conf -b
Comment=X11 compositor for XFCE
OnlyShowIn=XFCE;
StartupNotify=false
Terminal=false
"""
    with open(picom_desktop_path, "w") as f:
        f.write(content)
    print(f"Created picom autostart entry at {picom_desktop_path}")

def download_and_copy(option):
    repo_url = "https://github.com/NormallyDisblend/Xfce-Dotfiles.git"
    clone_dir = "/tmp/xfce-dotfiles"
    dest_map = {
        "config": os.path.expanduser("~/.config"),
        "background": os.path.expanduser("~/.config/xfce4/desktop"),
        "gtk_config": os.path.expanduser("~/.config/gtk-3.0"),
        "panel": os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml"),
        "compositor": os.path.expanduser("~/.config/picom.conf"),
        "fastfetch": os.path.expanduser("~/.config/fastfetch"),
        "kitty": os.path.expanduser("~/.config/kitty"),
    }
    config_subfolder_map = {
        "config": "config",
        "background": "background",
        "gtk_config": "gtk_config",
        "panel": "panel",
        "compositor": "compositor",
        "fastfetch": "fastfetch",
        "kitty": "kitty",
    }
    if option not in dest_map or dest_map[option] is None:
        print(f"Skipping {option}: no destination folder defined.")
        return
    dest_folder = dest_map[option]
    src_subfolder = config_subfolder_map[option]
    print(f"Processing {option}...")
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    subprocess.run(["git", "clone", "--depth", "1", repo_url, clone_dir], check=True)
    src_folder = os.path.join(clone_dir, src_subfolder)
    if not os.path.exists(src_folder):
        print(f"Source folder {src_folder} not found in repo. Skipping {option}.")
        shutil.rmtree(clone_dir)
        return
    if os.path.isdir(src_folder):
        if os.path.exists(dest_folder):
            if os.path.isdir(dest_folder):
                shutil.rmtree(dest_folder)
            else:
                os.remove(dest_folder)
        shutil.copytree(src_folder, dest_folder)
    else:
        # For single file config like picom.conf
        if os.path.exists(dest_folder):
            os.remove(dest_folder)
        shutil.copy2(src_folder, dest_folder)
    print(f"Copied {option} config to {dest_folder}")
    shutil.rmtree(clone_dir)

def main():
    global
