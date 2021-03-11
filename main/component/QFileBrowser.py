import sys
import os

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

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


class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setMinimumWidth(800)

        hlay = QHBoxLayout(self)
        self.driveList = QListView()
        self.driveList.setMaximumWidth(180)
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

        path = "c"

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = MyFileSystemModel()
        self.fileModel.setFilter(QDir.NoDot |  QDir.Files | QDir.AllDirs)
        self.fileModel.setNameFilters(["*.ma"])
        self.fileModel.setNameFilterDisables(False)

        self.driveList.setModel(self.dirModel)
        self.fileList.setModel(self.fileModel)

        self.driveList.setRootIndex(self.dirModel.index(path))
        self.fileList.setRootIndex(self.fileModel.index(path))

        header = self.fileList.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.ResizeToContents)   
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignVCenter)
        self.fileList.setColumnWidth(1,80)
        self.fileList.setColumnWidth(2,80)

        self.driveList.clicked.connect(self.drive_click)
        self.fileList.selectionModel().selectionChanged.connect(self.file_click)
        self.fileList.doubleClicked.connect(self.file_expand)
        self.currentPath.textChanged.connect(self.change_path)

    def drive_click(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.fileList.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath.setText(path)

    def file_click(self, selection):
        path = self.fileModel.fileInfo(selection.indexes()[0]).absoluteFilePath()
        if self.fileModel.fileInfo(selection.indexes()[0]).isFile():
            self.currentFile.setText(os.path.basename(path))

    def file_expand(self, index):
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        if self.fileModel.fileInfo(index).isDir():
            self.currentPath.setText(path)
    
    def change_path(self):
        path = os.path.normpath(self.currentPath.text()).replace("\\", "/")
        if os.path.isdir(path):
            self.fileList.setRootIndex(self.fileModel.setRootPath(path))
        elif os.path.isfile(path):
            self.fileList.setRootIndex(self.fileModel.setRootPath(os.path.dirname(path)))
            self.currentFile.setText(os.path.basename(path))
            self.currentPath.setText(os.path.dirname(path))


w = Widget()
w.show()