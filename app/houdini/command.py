import hou

try:
    from PySide2.QtWidgets import QApplication
except:
    from PySide.QtGui import QApplication

def get_app_window():
    if hou.applicationVersion()[0] > 14:
        try:
            return hou.ui.mainQtWindow()
        except:
            pass
        
    app = QApplication.instance()
    for w in app.topLevelWidgets():
        if hasattr( w, 'windowIconText' ) and w.windowIconText():
            return w

def get_app_ext():
    return ['*.hip']

def check():
    pass

def clear_scene():
    if check():
        pass

def open_file(filepath = "", new_window = False):
    pass

def new_scene(new_window = False):
    pass

def get_open_file():
    pass