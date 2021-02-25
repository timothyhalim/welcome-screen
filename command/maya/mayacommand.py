
from PySide.QtGui import *
from PySide.QtCore import *

from time import sleep

from maya import cmds

def check():
    ok = True
    if cmds.file(mf=True, q=True):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("File is not saved continue?")
        msg.setWindowTitle("Continue?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        ret = msg.exec_() 
        ok = ret == 1024
    return ok

def clear_scene():
    if check():
        cmds.file(new=True, f=True)

def open_file(filepath = "", new_window = False):
    if get_open_file() and get_open_file() != filepath:
        if not new_window:
            clear_scene()
            cmds.file(filepath, o=True, f=True)
        else:
            if check():
                cmds.file(filepath, o=True, f=True)
    else:
        try:
            cmds.file(filepath, o=True, f=True)
        except:
            pass

def new_scene(new_window = False):
    if not new_window:
        clear_scene()
    else:
        clear_scene()

def get_open_file():
    return cmds.file(sn=True, q=True)