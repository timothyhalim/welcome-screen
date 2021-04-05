try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

import os
import re
    
class RecentLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, fileInfo={"path":"", 'access_date':""}):
        super(RecentLabel, self).__init__()
        self.setFixedHeight(30)
        self.filePath = ""
        self.setStyleSheet("background: transparent")
        if fileInfo:
            self.update_file(fileInfo)

    def update_file(self, fileInfo):
        self.filePath = fileInfo['path']
        self._textFont = "Arial"
        self._textSize = 5
        if self.filePath:
            self._text = "[%s] %s" %(fileInfo['access_date'], os.path.basename(self.filePath))
            self.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self._textSize, self._textFont, self._text))
            self.setToolTip(self.filePath)
        else:
            self._text = ""
            self.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self._textSize, self._textFont, self._text))

    def changeColor(self, color):
        if self._text:
            currentText = self.text()
            pattern = r"(#[a-zA-Z0-9]{6})"
            newText = re.sub(pattern, color, currentText)
            self.setText(newText)

    def enterEvent(self, event): self.changeColor("#FFC132")
    def leaveEvent(self,event): self.changeColor("#B4B4B4")
    def mousePressEvent(self, event): self.changeColor("#DFA112")
    def mouseReleaseEvent(self,event):
        self.changeColor("#FFC132")
        if self.filePath:
            self.clicked.emit(self.filePath)
        
class RecentList(QScrollArea):
    fileClicked = Signal(str)

    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent=None)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        self.viewport().setAutoFillBackground( False )
        self.setFrameStyle( QFrame.NoFrame )
        self.setWidgetResizable(True)
        self.createContainer()
        
    def createContainer(self):
        self.container = QWidget()
        self.container.setStyleSheet("background-color: rgba(0,0,0,2)")
        self.mainLayout = QVBoxLayout(self.container)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addStretch()
        self.setWidget(self.container)
    
    def clicked(self, value):
        self.fileClicked.emit(value)

    def addItem(self, fileInfo):
        btn = RecentLabel(fileInfo)
        self.mainLayout.insertWidget(0, btn)
        btn.clicked.connect(self.clicked)

    def addItems(self, fileInfos):
        for info in sorted(fileInfos, key=lambda k : k['access_date']):
            self.addItem(info)

    def clear(self):
        self.container.setParent(None)
        self.container = None
        self.createContainer()

class RecentWidget(QWidget):
    filterChanged = Signal(str)
    fileClicked = Signal(str)

    def __init__(self, parent=None):
        super(RecentWidget, self).__init__(parent=parent)
        self._items = []

        self.recent_search = QLineEdit()
        self.search_icon = os.path.normpath(os.path.join(__file__, "..", "..", "icons", "search.png")).replace("\\", "/")
        self.recent_search.setStyleSheet("""color:rgb(180, 180, 180); 
                                            padding:4px 4px 4px 20px; 
                                            background-image:url(%s); 
                                            background-color:transparent; 
                                            background-position: left; 
                                            background-repeat:no-repeat""" % self.search_icon )
        self.recent_search.setPlaceholderText("Search Recent Files")

        self.recent_list = RecentList()

        self.recent_widget_layout = QVBoxLayout(self)
        self.recent_widget_layout.setContentsMargins(0,0,0,0)
        self.recent_widget_layout.addWidget(self.recent_search)
        self.recent_widget_layout.addWidget(self.recent_list)

        self.recent_search.textChanged.connect(self.filterList)
        self.recent_list.fileClicked.connect(self.fileClick)

    def addItem(self, fileInfo):
        self._items.append(fileInfo)
        self.filterList()

    def addItems(self, fileInfos):
        self._items.extend(fileInfos)
        self.filterList()

    def clear(self):
        self._items = []
        self.recent_list.clear()

    def fileClick(self, file):
        self.fileClicked.emit(file)

    def filterList(self):
        fileList = self._items
        if self.recent_search.text():
            fileList = [f for f in self._items if self.recent_search.text().lower() in f['path'].lower()]
        self.recent_list.clear()
        self.recent_list.addItems(fileList)