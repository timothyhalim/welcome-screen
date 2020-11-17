from PySide.QtGui import *
from PySide.QtCore import *

import os

ICON_PATH = os.path.normpath(os.path.join(__file__, "..", "..", "icons"))

class QCustomLabel(QWidget):
    clicked = Signal(object)

    def __init__(self, name=None, icon="", iconsize=50):
        super(QCustomLabel, self).__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.imageFile = "%s/%s.png" % (ICON_PATH, icon)
        if os.path.isfile(self.imageFile):
            self.icon = QLabel()
            self.icon.setFixedWidth(iconsize)
            self.icon.setFixedHeight(iconsize)
            self.icon.setPixmap(QPixmap(self.imageFile).scaled(iconsize, iconsize , Qt.KeepAspectRatio))
            self.layout.addWidget(self.icon)

        if isinstance(name, str):
            self.label = QLabel()
            self.label.text = name
            self.layout.addWidget(self.label)
            self.label.textFont = "Arial"
            self.label.textSize = 5
            self.label.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.label.textSize, self.label.textFont, self.label.text))
            # self.label.setToolTip(name)
            self.label.setFixedWidth(110)

            # self.connect(self.newCompLabel, SIGNAL('labelClicked()'), self.newComp)
            self.label.setStyleSheet("padding: 0px 0px 0px 15px")

            self.label.mouseReleaseEvent = self.mouseReleaseEvent
        else:
            self.label = None

    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgb(80, 80, 80, 255); border-radius: 3px;")
        if not self.label is None:
            self.label.setText('<font color = #FFC132 size = %s face = %s>%s</font>' % (self.label.textSize, self.label.textFont, self.label.text))

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: rgb(54, 54, 54, 0); border-radius: 3px;")
        if not self.label is None:
            self.label.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.label.textSize, self.label.textFont, self.label.text))

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color: rgb(30, 30, 30, 255); border-radius: 3px;")
        if not self.label is None:
            self.label.setText('<font color = #DFA112 size = %s face = %s>%s</font>' % (self.label.textSize, self.label.textFont, self.label.text))

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("background-color: rgb(80, 80, 80, 255); border-radius: 3px;")
        if not self.label is None:
            self.label.setText('<font color = #FFC132 size = %s face = %s>%s</font>' % (self.label.textSize, self.label.textFont, self.label.text))
        self.emit(SIGNAL('clicked()'))