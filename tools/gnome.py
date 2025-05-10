from langchain_core.tools import tool
import os 
import subprocess
from pathlib import Path

def tilde(directory: str):
    """Converts ~/ to /home/user/"""
    path = directory.replace("~/", str(Path.home()) + "/")
    if path.startswith("./") or path.startswith("/") == False:
        path = path.removeprefix(".")
        if path.startswith("/") == False:
            path = "/" + path
        path = (os.getcwd() + path).replace("//", "/")
    return path
# Gnome desktop Customization tools
@tool
def light_dark_theme(theme: str):
    """Sets desktop theme, valid values are "prefer-light" and "prefer-dark". """
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", theme], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return str(res.stdout) + "\n" + str(res.stderr)

@tool
def accent_color(color: str):
    """Sets desktop accent color, Valid values are "blue", "teal", "green", "yellow", "orange", "red", "pink", "purple", "slate" """
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "accent-color", color], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return str(res.stdout) + "\n" + str(res.stderr)
@tool
def wallpaper(file: str):
    """Sets desktop wallpaper to an image file."""

    if file.find("https://") != -1:
        return "Failed! Wallpaper cannot be a url, must be a local file!"
    if os.path.exists(file) == False:
        return "File does not exist, are you using the correct name?"
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://" + tilde(file)], capture_output=True, text=True)
    res = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", "file://" + tilde(file)], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Success"
    return str(res.stdout) + "\n" + str(res.stderr)
