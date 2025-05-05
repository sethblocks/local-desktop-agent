from langchain_core.tools import tool
from pathlib import Path
import os


#Tools for accessing files

def tilde(directory: str):
    """Converts ~/ to /home/user/"""
    path = directory.replace("~/", str(Path.home()) + "/")
    if path.startswith("./"):
        path = path.removeprefix(".")
        path = os.getcwd() + path
    return path
@tool
def find_file(name: str, path: str):
    """finds files on the drive, not case sensitive, uses exact match. Path is the path to search, if unsure, use "~/" """
    response = ""
    if path == "~":
        path = "~/"
    closest = 0
    for fd in os.walk(tilde(path)):
        if fd[0].startswith(tilde("~/.")) != True: # Hidden files are hidden for a reason
            for f in fd[2]:
                matching = 0
                for word in name.split(" "):
                    if f.split("/")[-1].lower().find(word.lower()) != -1:
                        matching+=1
                if matching > int(len(name.split(" "))/2):
                    print(f)
                    if matching >= closest:
                        response = "\n" + (fd[0] + "/" + f) + response
                    else:
                        response +="\n" + (fd[0] + "/" + f)
    

    return "Files Found:" + response
@tool
def ls(dir: str):
    """Same functionality as the ls command, requires a full path or path using ~/"""
    try:
        return "\n".join(os.listdir(tilde(dir)))
    except:
        return "Folder does not exist"


@tool
def write(file: str, text: str):
    """Creates/Overwrites a file, writes the text raw, AS GIVEN, no modifications or operations are done to the text value."""
    try:
        open(tilde(file), "w").write(text)
        return "Written Succesfully to " + tilde(file)
    except:
        return "Unable to write! Maybe the file is root-only?"
@tool
def read(file: str):
    """Reads contents of a file"""
    try:
        return open(tilde(file), "r").read()
    except:
        return "Unable to read! Maybe the file is root-only or nonexistent?"
@tool
def mkdir(new_path: str):
    """Creates a folder, new path should be a full path or start with ~/"""
    try:
        os.mkdir(path=tilde(new_path))
        return "Success: " + new_path
    except Exception as e:
        return "Error: " + str(e)


if __name__ == "__main__":
    #test stuff
    pass