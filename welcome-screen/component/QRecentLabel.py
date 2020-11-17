from PySide.QtGui import *
from PySide.QtCore import *

import os

class QRecentLabel(QLabel):
    def __init__(self):
        super(QRecentLabel, self).__init__()
        self.filePath = ""

    def update_file(self, file={"path":""}):
        self.filePath = file['path']
        self.textFont = "Arial"
        self.textSize = 5
        if self.filePath:
            self.text = "[%s] %s" %(file['access_date'], os.path.basename(self.filePath))
            self.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))
            self.setToolTip(self.filePath)
        else:
            self.text = ""
            self.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))

    def enterEvent(self, event):
        self.setText('<font color = #FFC132 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))

    def leaveEvent(self,event):
        self.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))

    def mousePressEvent(self, event):
        self.setText('<font color = #DFA112 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))

    def mouseReleaseEvent(self,event):
        self.setText('<font color = #FFC132 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))
        self.emit(SIGNAL('openScript()'))
        