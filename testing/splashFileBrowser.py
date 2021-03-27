execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\SplashScreen.py")
execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\FileBrowser.py")

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

class WelcomeScreen(SplashScreen):
    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent)
        self.setObjectName("WelcomeScreen")
        self.setup_ui()

    def setup_ui(self):
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.setContentsMargins(0,0,0,15)
        self.file_browser = FileBrowser()
        self.master_layout.addWidget(self.file_browser)
