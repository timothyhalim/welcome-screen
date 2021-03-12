import sys
import os
import re

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

class FileSystemModel(QFileSystemModel):
    def __init__(self, h_align = Qt.AlignLeft, v_align = Qt.AlignVCenter, parent = None):
        super(FileSystemModel, self).__init__(parent)
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
            if index.column() ==  1 :
                return int(Qt.AlignRight | Qt.AlignVCenter)

        else:
            return super(FileSystemModel, self).data(index, role)


class FileList(QTableView):
    pathChanged = Signal(str)
    executed = Signal(str)

    def __init__(self, parent=None, filterExtension=[]):
        super(FileList, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filterExtension = filterExtension

        # Model
        self.fileModel = FileSystemModel()
        self.fileModel.setFilter(QDir.NoDot | QDir.Files | QDir.AllDirs)
        if self.filterExtension:
            self.fileModel.setNameFilters(self.filterExtension)
        self.fileModel.setNameFilterDisables(False)
        self.fileModel.setRootPath("")
        self.setModel(self.fileModel)
        self.tableSelectionModel = self.selectionModel()

        # Gui
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(24)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setShowGrid(False)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

        header = self.horizontalHeader()
        try:
            header.setSectionResizeMode(0, QHeaderView.Stretch)
        except:
            header.setResizeMode(0, QHeaderView.Stretch)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,80)

        # Signal
        self.fileModel.rootPathChanged.connect(self.on_root_changed)
        self.tableSelectionModel.currentChanged.connect(self.on_selection_changed)
        self.doubleClicked.connect(self.on_double_click)

        # Init
        self.set_root("")
    
    def root(self):
        return self.fileModel.rootPath()

    def set_root(self, path):
        prev = self.fileModel.rootPath()
        if not path or (path.endswith("..") and self.isdrive(path.replace("..", ""))):
            self.fileModel.setRootPath("")
            if prev and self.isdrive(prev):
                self.select_path(prev)
            else:
                self.select_path(QDir.drives()[0].filePath())
        else:
            path = os.path.abspath(path)
            forward = os.path.abspath(prev) in path if prev else True
            if os.path.isfile(path):
                root = os.path.dirname(path)
                self.fileModel.setRootPath(root)
            else:
                self.fileModel.setRootPath(path)
            if forward:
                self.select_first_row()
            else:
                self.select_path(prev)
        self.pathChanged.emit(self.path)
        
    def isdrive(self, path):
        path.replace("\\", "/")
        drives = [d.filePath() for d in QDir.drives()]
        return path in drives

    def on_root_changed(self, newpath):
        self.setRootIndex(self.fileModel.index(newpath))

    def on_selection_changed(self, current, prev):
        self.path = self.fileModel.filePath(current)
        self.pathChanged.emit(self.path)

    def on_double_click(self, index):
        if self.path.endswith("..") and self.isdrive(self.path.replace("..", "")):
            self.set_root("")
        elif os.path.isdir(self.path) or self.isdrive(self.path):
            self.set_root(self.path)
        elif os.path.isfile(self.path):
            self.executed.emit(self.path)

    def filter_path(self, path):
        if not self.filterExtension: return True
        for pattern in self.filterExtension:
            if re.search(pattern, path):
                return True

    def select_first_row(self):
        root = self.fileModel.rootPath()
        qd = QDir(root)
        qd.setNameFilters(self.filterExtension)
        qd.setSorting(QDir.DirsFirst)
        contents = qd.entryInfoList(QDir.Dirs | QDir.Files | QDir.NoDotAndDotDot | QDir.Drives)
        if contents:
            self.select_path(contents[0].filePath())

    def select_path(self, path):
        index = self.fileModel.index(path)
        self.tableSelectionModel.setCurrentIndex(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        # self.tableSelectionModel.select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.scrollTo(index)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if os.path.isdir(self.path):
                self.set_root(self.path)
            else:
                self.executed.emit(self.path)

        elif event.key() == Qt.Key_Backspace:
            if self.fileModel.rootPath():
                root = os.path.abspath(self.fileModel.rootPath())
                paths = [d for d in root.split("\\") if d]
                if len(paths) > 1:
                    parentdir = "/".join(paths+[".."])
                else:
                    parentdir = ""

                self.set_root(parentdir)
        elif event.key() == Qt.Key_Escape:
            self.parent().setFocus()
        else:
            super(FileList, self).keyPressEvent(event)

class FileBrowser(QWidget):
    executed = Signal(str)
    def __init__(self, parent=None, filterExtension=[], exeLabel="Open", title="Open File"):
        QWidget.__init__(self, parent=None)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.currentPath = QLineEdit()
        self.fileList = FileList(filterExtension=filterExtension)
        self.fileLayout = QHBoxLayout()
        self.currentFile = QLineEdit()
        self.exeButton = QPushButton(exeLabel)
        self.fileLayout.addWidget(self.currentFile)
        self.fileLayout.addWidget(self.exeButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.currentPath)
        self.mainLayout.addWidget(self.fileList)
        self.mainLayout.addLayout(self.fileLayout)

        for l in [self.currentFile, self.currentPath]:
            l.setFixedHeight(26)

        self.currentPath.textChanged.connect(self.change_path)
        self.fileList.pathChanged.connect(self.on_change_path)
        self.fileList.executed.connect(self.execute)
        self.exeButton.clicked.connect(self.execute)
        self.exeButton.setMinimumWidth(70)

        self.on_change_path(self.fileList.path)

        self.currentPath.installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.currentPath:
            if (event.type() == QEvent.FocusOut):
                self.fileList.pathChanged.connect(self.on_change_path)
            elif (event.type() == QEvent.FocusIn):
                self.fileList.pathChanged.disconnect()
        elif source is self.fileList:
            if (event.type() == QEvent.FocusOut):
                self.currentPath.textChanged.connect(self.change_path)
            elif (event.type() == QEvent.FocusIn):
                self.currentPath.textChanged.disconnect()
        return super(FileBrowser, self).eventFilter(source, event)

    def on_change_path(self, newpath):
        self.currentPath.textChanged.disconnect()
        if os.path.isdir(newpath) or self.fileList.isdrive(newpath):
            path = self.fileList.root() + "/" if self.fileList.root() and not self.fileList.root().endswith("/") else self.fileList.root()
            self.currentPath.setText(path.replace("/", "\\"))
            self.currentFile.setText("")
        elif os.path.isfile(newpath):
            self.currentPath.setText((os.path.dirname(newpath)+"/").replace("/", "\\"))
            self.currentFile.setText(os.path.basename(newpath))
        self.currentPath.textChanged.connect(self.change_path)

    def change_path(self):
        if self.currentPath.text():
            path = os.path.abspath(self.currentPath.text())
            if os.path.exists(path):
                self.fileList.set_root(path)
        else:
            self.fileList.set_root("")
    
    def set_root(self, path):
        self.fileList.set_root(path)

    def execute(self):
        if os.path.isfile(self.fileList.path):
            self.executed.emit(self.fileList.path)
        else:
            self.fileList.set_root(self.fileList.path)