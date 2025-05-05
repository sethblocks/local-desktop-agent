from langchain_core.tools import tool
import os 
import subprocess
from pathlib import Path

def tilde(directory: str):
    """Converts ~/ to /home/user/"""
    path = directory.replace("~/", str(Path.home()) + "/")
    if path.startswith("./"):
        path = path.removeprefix(".")
        path = os.getcwd() + path
    return path
# Gnome desktop Customization tools
@tool
def light_dark_theme(theme: str):
    """Sets desktop theme, valid values are "prefer-light" and "prefer-dark". """
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", theme], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return res.stdout + "\n" + res.stderr

@tool
def accent_color(color: str):
    """Sets desktop accent color, Valid values are "blue", "teal", "green", "yellow", "orange", "red", "pink", "purple", "slate" """
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "accent-color", color], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return res.stdout + "\n" + res.stderr
@tool
def wallpaper(file: str):
    """Sets desktop wallpaper to a local image file. Requires a full path or a path starting with ~/"""
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://" + tilde(file)], capture_output=True, text=True)
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", "file://" + tilde(file)], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return res.stdout + "\n" + res.stderr
if __name__ == "__main__":
    pass#print(wallpaper("/home/seth/Pictures/Screenshots/Screenshot From 2025-04-24 20-52-25.png"))