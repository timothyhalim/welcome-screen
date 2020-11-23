from PySide.QtGui import *
from PySide.QtCore import *
import os

Global_Icon_Path = os.path.normpath(os.path.join(__file__, "..", "..", "icons"))

class AboutWidget(QWidget):
    def __init__(self):
        super(AboutWidget, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(270, 250)
        self.setWindowTitle("About")

        self.setStyleSheet("color: white; background-color: rgb(50, 50, 50)")
        aboutToolbox = QLabel()
        aboutToolbox.setPixmap(QPixmap("%s/aboutWS.png" % Global_Icon_Path).scaled(250, 100, Qt.KeepAspectRatio))
        aboutVer = QLabel(VER)
        aboutVer.setStyleSheet("font:20px Arial")
        aboutAuthor = QLabel("Author:%s" % AUTHOR)
        aboutAuthor.setAlignment(Qt.AlignRight)
        aboutAuthor.setStyleSheet("font:15px Arial")
        aboutDate = QLabel("Date:%s" % DATE)
        aboutDate.setAlignment(Qt.AlignRight)
        aboutDate.setStyleSheet("font:15px Arial")

        self.masterLayout = QVBoxLayout()
        self.masterLayout.addWidget(aboutToolbox)
        self.masterLayout.addWidget(aboutVer)
        self.masterLayout.addWidget(aboutAuthor)
        self.masterLayout.addWidget(aboutDate)
        self.setLayout(self.masterLayout)

        self.adjustSize()
        screenRes = QDesktopWidget().screenGeometry()
        #self.move(QPoint(screenRes.width()/2,screenRes.height()/2)-QPoint((self.width()/2),(self.height()/2)))
        self.move(QPoint(0, 0))