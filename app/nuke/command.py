import nuke

try:
    from Pyside2.QtWidgets import QApplication, QMessageBox
except:
    from PySide.QtGui import QApplication

def get_app_window():
    for w in QApplication.topLevelWidgets():
        if w.metaObject().className() == 'Foundry::UI::DockMainWindow':
            return w

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