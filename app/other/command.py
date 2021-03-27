try:
    from PySide2.QtWidgets import QApplication
except:
    from PySide.QtGui import QApplication

def get_app_window():
    app = QApplication.instance()
    for w in app.topLevelWidgets():
        return w

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