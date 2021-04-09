try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

import os
import re
    
class RecentLabel(QWidget):
    fileClicked = Signal(str)

    def __init__(self, fileInfo={"path":"", 'access_date':""}, checkable=False):
        super(RecentLabel, self).__init__()
        self.setFixedHeight(30)
        self.setStyleSheet("background: transparent")

        self.textFont = "Arial"
        self.textSize = 5

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.edit = QCheckBox()
        self.edit.setMaximumWidth(20)
        self.label = QLabel()

        for w in [self.edit, self.label]:
            self.layout().addWidget(w)

        self.updateInfo(fileInfo)
        self.setCheckable(checkable)
        self.label.installEventFilter(self)

    def setChecked(self, state):
        self.edit.setChecked(state)

    def isChecked(self):
        return self.edit.isChecked()

    def setCheckable(self, state):
        if state:
            self.setEnabled(state)
        self.edit.setVisible(state)
        self.checkable = state

    def updateInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.text = ""
        if self.fileInfo['path']:
            self.setToolTip(self.fileInfo['path'])
            self.text = "[%s] %s" %(self.fileInfo['access_date'], os.path.basename(self.fileInfo['path']))

        self.label.setText('<font color = #B4B4B4 size = %s face = %s>%s</font>' % (self.textSize, self.textFont, self.text))
        self.changeColor("#B4B4B4")

    def changeColor(self, color):
        currentText = self.label.text()
        pattern = r"(#[a-zA-Z0-9]{6})"
        newText = re.sub(pattern, "#808080", currentText)
        self.setEnabled(False)
        if os.path.exists(self.fileInfo['path']):
            self.setEnabled(True)
            newText = re.sub(pattern, color, currentText)
        self.label.setText(newText)

    def eventFilter(self, obj, event):
        if obj is self.label:
            if event.type() == QEvent.Enter:
                self.changeColor("#FFC132")
            elif event.type() == QEvent.Leave:
                self.changeColor("#B4B4B4")
            elif event.type() == QEvent.MouseButtonPress:
                self.changeColor("#FFC132")
            elif event.type() == QEvent.MouseButtonRelease:
                self.changeColor("#FFC132")
                if self.checkable:
                    self.setChecked(not self.isChecked())
                else:
                    if self.fileInfo['path']:
                        self.fileClicked.emit(self.fileInfo['path'])
        return super(RecentLabel, self).eventFilter(obj, event)
        
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

        self.items = []
        
    def createContainer(self):
        self.container = QWidget()
        self.container.setStyleSheet("background-color: rgba(0,0,0,2)")
        self.mainLayout = QVBoxLayout(self.container)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addStretch()
        self.setWidget(self.container)
    
    def clicked(self, value):
        self.fileClicked.emit(value)

    def addItem(self, fileInfo, checkable):
        btn = RecentLabel(fileInfo, checkable=checkable)
        self.items.insert(0, btn)
        self.mainLayout.insertWidget(0, btn)
        btn.fileClicked.connect(self.clicked)

    def removeItem(self, btn):
        self.mainLayout.removeWidget(btn)
        self.items.remove(btn)
        btn.setParent(None)

    def clear(self):
        self.items = []
        self.container.setParent(None)
        self.container = None
        self.createContainer()

class RecentWidget(QWidget):
    filterChanged = Signal(str)
    fileClicked = Signal(str)
    removeFiles = Signal(list)

    def __init__(self, parent=None):
        super(RecentWidget, self).__init__(parent=parent)
        self._items = []
        self.search_icon_path = os.path.normpath(os.path.join(__file__, "..", "..", "icons", "search.png")).replace("\\", "/")
        self.edit_icon_path = os.path.normpath(os.path.join(__file__, "..", "..", "icons", "pencil.png")).replace("\\", "/")

        self.edit_icon = QPixmap(self.edit_icon_path)
        self.edit_icon_mask = self.edit_icon.createMaskFromColor(QColor('transparent'), Qt.MaskInColor)

        self.top_layout = QHBoxLayout()
        self.recent_search = QLineEdit()
        self.recent_search.setStyleSheet("""color:rgb(221, 221, 221); 
                                            padding:4px 4px 4px 20px; 
                                            background-image:url(%s); 
                                            background-color:transparent; 
                                            background-position: left; 
                                            background-repeat:no-repeat""" % self.search_icon_path )
        self.recent_search.setPlaceholderText("Search Recent Files")

        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon(self.edit_icon))
        self.edit_button.setCheckable(True)
        for w in [self.recent_search, self.edit_button]:
            self.top_layout.addWidget(w)

        self.recent_list = RecentList()

        self.bottom_layout = QHBoxLayout()
        self.select_all = QPushButton("All")
        self.select_missing = QPushButton("Missing")
        self.select_none = QPushButton("None")
        self.remove_selection = QPushButton("Remove Checked Items")
        for w in [self.select_all, self.select_missing, self.select_none, self.remove_selection]:
            self.bottom_layout.addWidget(w)

        self.recent_widget_layout = QVBoxLayout(self)
        self.recent_widget_layout.setContentsMargins(0,0,0,0)
        self.recent_widget_layout.addLayout(self.top_layout)
        self.recent_widget_layout.addWidget(self.recent_list)
        self.recent_widget_layout.addLayout(self.bottom_layout)

        self.recent_search.textChanged.connect(self.filterList)
        self.recent_list.fileClicked.connect(self.fileClick)
        self.edit_button.clicked.connect(self.setEditable)
        self.select_all.clicked.connect(self.checkAll)
        self.select_missing.clicked.connect(self.checkMissing)
        self.select_none.clicked.connect(self.checkNone)
        self.remove_selection.clicked.connect(self.removeChecked)

        self.setEditable()

    def addItem(self, fileInfo):
        self._items.append(fileInfo)
        self.recent_list.addItem(fileInfo, self.edit_button.isChecked())
        self.filterList()

    def addItems(self, fileInfos):
        fileInfos.sort(key=lambda k:k['access_date'])
        for fileInfo in fileInfos:
            self.addItem(fileInfo)

    def removeItems(self, fileInfos):
        for fileInfo in fileInfos:
            self.recent_list.removeItem(fileInfo)

    def clear(self):
        self._items = []
        self.recent_list.clear()

    def fileClick(self, file):
        self.fileClicked.emit(file)

    def filterList(self):
        fileInfos = self._items
        if self.recent_search.text():
            fileInfos = [f for f in self._items if self.recent_search.text().lower() in f['path'].lower()]
        for item in self.recent_list.items:
            if item.fileInfo in fileInfos:
                item.setVisible(True)
            else:
                item.setVisible(False)

    def setEditable(self):
        state = self.edit_button.isChecked()
        if state:
            self.edit_icon.fill((QColor(255, 193, 50)))
        else:
            self.edit_icon.fill((QColor(221, 221, 221)))
        self.edit_icon.setMask(self.edit_icon_mask)
        self.edit_button.setIcon(QIcon(self.edit_icon))

        for item in self.recent_list.items:
            item.setCheckable(state)

        for w in [self.select_all, self.select_missing, self.select_none, self.remove_selection]:
            w.setVisible(state)

    def checkAll(self):
        for item in self.recent_list.items:
            if item.isVisible():
                item.setChecked(True)

    def checkNone(self):
        for item in self.recent_list.items:
            if item.isVisible():
                item.setChecked(False)

    def checkMissing(self):
        for item in self.recent_list.items:
            if item.isVisible():
                if not os.path.exists(item.fileInfo['path']):
                    item.setChecked(True)

    def removeChecked(self):
        checked = [item for item in self.recent_list.items if item.isChecked()]
        self.removeItems(checked)

        self.removeFiles.emit([item.fileInfo['path'] for item in checked])

        self.edit_button.setChecked(False)
        self.setEditable()
        
