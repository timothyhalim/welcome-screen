import sys
import os

try:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"
except:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"

print(qttype)

class MyFileSystemModel(QFileSystemModel):
    def __init__(self, h_align = Qt.AlignLeft, v_align = Qt.AlignVCenter, parent = None):
        super(MyFileSystemModel, self).__init__(parent)
        self.alignments = {Qt.Horizontal:h_align, Qt.Vertical:v_align}

    def headerData(self, section, orientation, role):
        if role == Qt.TextAlignmentRole:
            return self.alignments[orientation]
        elif role == Qt.DecorationRole:
            return None
        else:
            return QFileSystemModel.headerData(self, section, orientation, role)

    def data(self, index, role):

        if role == Qt.TextAlignmentRole:
            if index.column() > 0 :
                return int(Qt.AlignRight | Qt.AlignVCenter)
            else:
                return int(Qt.AlignLeft | Qt.AlignVCenter)

        else:
            return super(MyFileSystemModel, self).data(index, role)


class FileBrowser(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        
        path = "?"

        self.setMinimumWidth(800)

        hlay = QHBoxLayout(self)

        # Drive List
        self.driveList = QListView()
        self.driveList.setMaximumWidth(180)

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.driveList.setModel(self.dirModel)
        # self.driveList.setRootIndex(self.dirModel.index(path))
        index = self.dirModel.index("C:/")
        # self.driveList.selectionModel().setCurrentIndex(0,0)
        
        hlay.addWidget(self.driveList)
        
        vlay = QVBoxLayout(self)
        hlay.addLayout(vlay)

        self.currentPath = QLineEdit()
        self.fileList = QTableView ()
        self.fileList.verticalHeader().setVisible(False)
        self.fileList.verticalHeader().setDefaultSectionSize(24)
        self.fileList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fileList.setShowGrid(False)
        self.fileList.setSortingEnabled(True)
        
        self.currentFile = QLineEdit()
        vlay.addWidget(self.currentPath)
        vlay.addWidget(self.fileList)
        vlay.addWidget(self.currentFile)

        self.fileModel = MyFileSystemModel()
        self.fileModel.setFilter(QDir.NoDot |  QDir.Files | QDir.AllDirs | QDir.Drives)
        self.fileModel.setNameFilters(["*.ma"])
        self.fileModel.setNameFilterDisables(False)
        self.fileList.setModel(self.fileModel)
        self.fileList.setRootIndex(self.fileModel.index(path))

        header = self.fileList.horizontalHeader()
        try:
            header.setSectionResizeMode(0, QHeaderView.Stretch)
        except:
            header.setResizeMode(0, QHeaderView.Stretch)
        self.fileList.setColumnWidth(1,80)
        self.fileList.setColumnWidth(2,80)

        self.driveList.clicked.connect(self.drive_click)
        # self.fileList.selectionModel().selectionChanged.connect(self.change_selection)
        # self.fileList.clicked.connect(self.change_selection)
        self.fileList.doubleClicked.connect(self.file_expand)
        self.currentPath.textChanged.connect(self.change_path)

        self.fileList.selectionModel().currentChanged.connect(self.selection_changed)

    def drive_click(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.fileList.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath.setText(path)

    def selection_changed(self, index, *args):
        print("selected: ", )
        self._currentPath = os.path.join( self.fileModel.rootPath(), index.data() ).replace("\\","/")

    # def change_selection(self, index):
    #     path = self.fileModel.fileInfo(index).absoluteFilePath()
    #     if self.fileModel.fileInfo(index).isFile():
    #         self.currentFile.setText(os.path.basename(path))

    def file_expand(self, index):
        print("DBLCLICK")
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        if self.fileModel.fileInfo(index).isDir():
            self.currentPath.setText(path)

        print(path)
    
    def change_path(self):
        if self.currentPath.text():
            path = os.path.normpath(self.currentPath.text()).replace("\\", "/")
            if os.path.isdir(path):
                self.fileList.setRootIndex(self.fileModel.setRootPath(path))
            elif os.path.isfile(path):
                self.fileList.setRootIndex(self.fileModel.setRootPath(os.path.dirname(path)))
                index = self.fileModel.index(path)
                print(index)
                self.fileList.selectionModel().setCurrentIndex(index, 0)
                self.currentFile.setText(os.path.basename(path))
                self.currentPath.setText(os.path.dirname(path))
        else:
            self.fileList.setRootIndex(self.fileModel.setRootPath("."))
            self.currentFile.setText("")
            self.currentPath.setText("")

    def keyPressEvent(self, event):
        #super(FileBrowser).keyPressEvent(event)
        print(event.key())
        if event.key() == Qt.Key_Enter: 
            print("Enter")
        elif event.key() == Qt.Key_Return:
            print("Return")
            if os.path.isdir(self._currentPath):
                self.currentPath.setText(self._currentPath)
                self.currentFile.setText("")
            elif os.path.isfile(self._currentPath):
                self.currentPath.setText(os.path.dirname(self._currentPath))
                self.currentFile.setText(os.path.basename(self._currentPath))

        # (
        #     Qt.Key_Tab,
        #     Qt.Key_Return,
        #     Qt.Key_Enter,
        # ):

w = FileBrowser()
w.show()