import sys
import os

try:
    main_folder = os.path.normpath(os.path.join(__file__, ".."))
except:
    import inspect
    main_folder = os.path.normpath(os.path.join(inspect.getframeinfo(inspect.currentframe()).filename, ".."))

if not main_folder in sys.path:
    sys.path.append(main_folder)
    
### Import Required Modules ###
try:
    from PySide2.QtWidgets import QApplication, QDialog
except:
    from PySide.QtGui import QApplication, QDialog

class MyMainWindow(QDialog):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

app = QApplication(sys.argv)
    
from main import WelcomeScreen

ws = WelcomeScreen(parent=None)
ws.start()
sys.exit(app.exec_())