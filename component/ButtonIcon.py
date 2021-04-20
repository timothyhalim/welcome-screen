try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

import os

try:
    ICON_PATH = os.path.normpath(os.path.join(__file__, "..", "..", "icons"))
except:
    import inspect
    ICON_PATH = os.path.normpath(os.path.join(inspect.getframeinfo(inspect.currentframe()).filename, "..", "..", "icons"))


class ButtonIcon(QPushButton):
    def __init__(self, name=None, icon="", iconsize=40):
        super(ButtonIcon, self).__init__()

        self.bold = False
        self.setCheckable(True)
        self.setMinimumSize(155,40)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.imageFile = "%s/%s.png" % (ICON_PATH, icon)
        if os.path.isfile(self.imageFile):
            self.icon = QIcon(QPixmap(self.imageFile).scaled(iconsize, iconsize , Qt.KeepAspectRatio))
            self.setIcon(self.icon)
            self.setIconSize(QSize(iconsize, iconsize))   

        if isinstance(name, str):
            font = self.font()
            font.setPointSize(10)
            self.setFont(font)
            self.setText(name)

        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid transparent;
                padding-left: 5px;
                padding-right: 5px;
                text-align:left;
            }
            QPushButton:checked{
                color: #FFC132;
                border-color: #FFC132;
                background-color: #232323;
                font-weight: bold;
            }
            QPushButton:pressed {
                color: #FFC132;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #FFC132;
            }
        """)
    
    def boldToggle(self, state):
        self.setChecked(state)