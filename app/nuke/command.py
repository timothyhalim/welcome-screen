
from PySide.QtGui import *
from PySide.QtCore import *

import nuke

def check():
    ok = True
    if nuke.modified():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("File is not saved continue?")
        msg.setWindowTitle("Continue?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        ret = msg.exec_() 
        ok = ret == 1024
    return ok

def clear_script():
    if check():
        nuke.scriptClear()

def open_file(filepath = "", new_window = False):
    if get_open_file() and get_open_file() != filepath:
        if not new_window:
            clear_script()
            nuke.scriptOpen(filepath)
        else:
            if check():
                nuke.scriptOpen(filepath)
    else:
        try:
            nuke.scriptOpen(filepath)
        except:
            pass

def new_scene(new_window = False):
    if not new_window:
        clear_script()
    else:
        nuke.scriptNew()

def get_open_file():
    return nuke.Root().knob("name").value()