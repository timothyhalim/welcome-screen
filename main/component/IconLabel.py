try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

import os
import re

ICON_PATH = os.path.normpath(os.path.join(__file__, "..", "..", "icons"))

class IconLabel(QWidget):
    clicked = Signal(object)

    def __init__(self, name=None, icon="", iconsize=50):
        super(IconLabel, self).__init__()

        self.bold = False

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
            self.text = name
            self.layout.addWidget(self.label)
            self.textFont = "Arial"
            self.textSize = 5
            self.label.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))
            # self.label.setToolTip(name)
            self.label.setFixedWidth(110)

            # self.connect(self.newCompLabel, SIGNAL('labelClicked()'), self.newComp)
            self.label.setStyleSheet("padding: 0px 0px 0px 15px")

            self.label.mouseReleaseEvent = self.mouseReleaseEvent
        else:
            self.label = None
    
    def boldToggle(self, state):
        if self.bold != state:
            self.bold = state
            currentText = self.label.text()
            if self.bold:
                self.label.setText("<b><u>%s</u></b>" %(currentText))
            elif not self.bold:
                pattern = r"^<b><u>(.*?)</u></b>$"
                result = re.search(pattern, currentText)
                if result:
                    self.label.setText(result.group(1))

    def changeColor(self, color):
        if not self.label is None:
            currentText = self.label.text()
            pattern = r"(#[a-zA-Z0-9]{6})"
            newText = re.sub(pattern, color, currentText)
            self.label.setText(newText)


    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgb(80, 80, 80, 255); border-radius: 3px;")
        self.changeColor("#FFC132")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: rgb(54, 54, 54, 0); border-radius: 3px;")
        self.changeColor("#B4B4B4")

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color: rgb(30, 30, 30, 255); border-radius: 3px;")
        self.changeColor("#DFA112")

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("background-color: rgb(80, 80, 80, 255); border-radius: 3px;")
        self.changeColor("#FFC132")
        self.emit(SIGNAL('clicked()'))