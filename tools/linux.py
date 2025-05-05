from langchain_core.tools import tool
from pathlib import Path
import os
import subprocess

#General tools for Linux 

def tilde(directory: str):
    """Converts ~/ to /home/user/"""
    path = directory.replace("~/", str(Path.home()) + "/")
    if path.startswith("./"):
        path = path.removeprefix(".")
        path = os.getcwd() + path
    return path
@tool
def terminal(cmd: str):
    """Runs a command, sudo is not allowed for security"""
    if cmd.find("sudo ") != -1:
        return "Sudo is not allowed, command was not run."
    else:
        process = subprocess.run(["bash"] + cmd.split(" "))
        return str(process.stdout) + "\n" + str(process.stderr)
@tool 
def open(file: str):
    """Opens a file from a path using xdg-open"""
    process = subprocess.run(["xdg-open", tilde(file)])
    if process.stderr == None:
        return "Opened Successfully!"
    return str(process.stdout) + "\n" + str(process.stderr)