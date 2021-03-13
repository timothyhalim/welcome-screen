#execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\ListPagination.py")
try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

import os
    
class RecentLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, info={"path":"", 'access_date':""}):
        super(RecentLabel, self).__init__()
        self.setFixedHeight(30)
        self.filePath = ""
        self.setStyleSheet("background-color: rgba(0,0,0,0)")
        if info:
            self.update_file(info)

    def update_file(self, file={"path":"", 'access_date':""}):
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
        if self.filePath:
            self.clicked.emit(self.filePath)
        
        
class RecentList(QScrollArea):
    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent=None)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        self.viewport().setAutoFillBackground( False )
        self.setFrameStyle( QFrame.NoFrame )
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.create_container()
        
    def create_container(self):
        self.container = QWidget()
        self.container.setStyleSheet("background-color: rgba(0,0,0,2)")
        self.mainLayout = QVBoxLayout(self.container)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addStretch()
        self.setWidget(self.container)
    
    def add_item(self, fileInfo):
        btn = RecentLabel(fileInfo)
        self.mainLayout.insertWidget(0, btn)

    def add_items(self, fileInfos):
        for info in sorted(fileInfos, key=lambda k : k['access_date']):
            self.add_item(info)

    def clear(self):
        self.container.setParent(None)
        self.container = None
        self.create_container()
        
        
        
w = RecentList()
w.show()