import os
import re
from time import sleep

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

def reconnect(signal, newhandler=None, oldhandler=None):        
    try:
        if oldhandler is not None:
            while True:
                signal.disconnect(oldhandler)
        else:
            signal.disconnect()
    except:
        pass
    if newhandler is not None:
        signal.connect(newhandler)
        
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

    # def index(self, *args, **kwargs):
    #     return super(FileSystemModel, self).index(*args, **kwargs)

class FileTable(QTableView):
    pathChanged = Signal(str)
    executed = Signal(str)

    def __init__(self, parent=None, filterExtension=[]):
        super(FileTable, self).__init__(parent)

        self.path = ""
        self.prev = ""
        self.target = ""
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
        self.fileModel.directoryLoaded.connect(self.on_loaded)
        self.tableSelectionModel.currentChanged.connect(self.on_selection_changed)
        self.doubleClicked.connect(self.on_double_click)
        self.destroyed.connect(self.clearSelection)

        # Init
        self.set_root("")
        self.on_loaded("")

    def close(self):
        self.clearSelection()
        super(FileTable, self).close()
    
    def root(self):
        return self.fileModel.rootPath()
    
    def on_loaded(self, path):
        path = self.fileModel.rootPath()
        if (self.prev == "" and path == ""):
            self.select_path(QDir.drives()[0].filePath())
        else:
            forward = (self.prev in path) if self.prev else True
            if forward:
                self.select_first_row()
            else:
                prevselection = [f for f in self.prev.replace(path, "").split("/") if f]
                if prevselection:
                    self.prev = os.path.join(path, prevselection[0])
                self.select_path(self.prev)

    def on_load_select(self):
        self.select_path(self.target)
        reconnect(self.fileModel.directoryLoaded, self.on_loaded, self.on_load_select)
        self.target = ""

    def set_root(self, path):
        self.prev = self.fileModel.rootPath()
        if path == "" or (path.endswith("..") and self.isdrive(path.replace("..", ""))):
            self.fileModel.setRootPath("")
            if self.prev and self.isdrive(self.prev):
                self.select_path(self.prev)
            else:
                self.select_path(QDir.drives()[0].filePath())
        else:
            path = os.path.abspath(path)
            if os.path.isfile(path):
                root = os.path.dirname(path)
                self.fileModel.setRootPath(root)
            else:
                self.fileModel.setRootPath(path)
        
    def isdrive(self, path):
        path.replace("\\", "/")
        drives = [d.filePath() for d in QDir.drives()]
        return path in drives

    def on_root_changed(self, newpath):
        self.current_index = self.fileModel.index(newpath)
        self.setRootIndex(self.current_index)

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
        if os.path.isdir(path): return True
        for pattern in self.filterExtension:
            rePattern = re.compile( re.escape( pattern ).replace( '\\*', '.*' ).replace( '\\?', '.' ) )
            if re.search(rePattern, path):
                return True

    def select_first_row(self):
        root = self.fileModel.rootPath()
        self.parent_index = self.fileModel.index(root)
        numRows = self.fileModel.rowCount(self.current_index)
        
        if numRows >= 1:
            row = 0
            while row < 3 and row < numRows:
                self.current_index = self.fileModel.index(row, 0, self.parent_index)
                file = self.fileModel.data(self.current_index, 0)
                if file not in [".", ".."]:
                    break
                row += 1

            if file:
                filePath = os.path.join(root, file)
                self.select_path(filePath)

    def select_path(self, path):
        self.current_index = self.fileModel.index(path)
        self.tableSelectionModel.setCurrentIndex(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.tableSelectionModel.select(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.scrollTo(self.current_index)

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

        # elif event.key() == Qt.Key_Escape:
        #     if self.parent():
        #         self.parent().setFocus()
            
        elif event.key() == Qt.Key_Tab:
            if self.parent():
                siblings = [w for w in self.parent().findChildren(QWidget) if w.parent() == self.parent()]
                currentIndex = -1
                for i, sibling in enumerate(siblings):
                    if sibling == self:
                        currentIndex = i
                        siblings.pop(i)
                        break
                siblings[currentIndex].setFocus()

        else:
            super(FileTable, self).keyPressEvent(event)

class FileBrowser(QWidget):
    executed = Signal(str)
    def __init__(self, parent=None, filterExtension=[], exeLabel="Open", title="Open File"):
        QWidget.__init__(self, parent=None)
        # self.setAttribute(Qt.WA_DeleteOnClose)

        self.fileList = FileTable(filterExtension=filterExtension)

        self.fileLayout = QHBoxLayout()
        self.currentPath = QLineEdit()
        self.currentPath.setPlaceholderText("File Path")
        self.exeButton = QPushButton(exeLabel)
        self.fileLayout.addWidget(self.currentPath)
        self.fileLayout.addWidget(self.exeButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.fileList)
        self.mainLayout.addLayout(self.fileLayout)

        for l in [self.currentPath]:
            l.setFixedHeight(26)

        self.currentPath.textChanged.connect(self.on_text_changed)
        self.currentPath.returnPressed.connect(self.validate_path)
        self.fileList.pathChanged.connect(self.on_path_changed)
        self.fileList.executed.connect(self.execute)
        self.exeButton.clicked.connect(self.execute)
        self.exeButton.setMinimumWidth(70)

        self.on_path_changed(self.fileList.path)

        self.currentPath.installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.currentPath:
            if (event.type() == QEvent.FocusOut):
                self.fileList.pathChanged.connect(self.on_path_changed)
                self.validate_path()
            elif (event.type() == QEvent.FocusIn):
                self.fileList.pathChanged.disconnect()
        elif source is self.fileList:
            if (event.type() == QEvent.FocusOut):
                self.currentPath.textChanged.connect(self.on_text_changed)
            elif (event.type() == QEvent.FocusIn):
                self.currentPath.textChanged.disconnect()
        return super(FileBrowser, self).eventFilter(source, event)
    
    def validate_path(self):
        self.change_current_path(self.fileList.path)
        if os.path.isfile(self.fileList.path):
            self.execute()
        else:
            self.fileList.setFocus()
    
    def change_current_path(self, text):
        self.currentPath.textChanged.disconnect()
        self.currentPath.setText(text)
        self.currentPath.textChanged.connect(self.on_text_changed)
        
    def on_path_changed(self, newpath):
        newpath = re.sub("(.*?)/(\.)+$", r"\1/", newpath)
        self.change_current_path(newpath)

    def on_text_changed(self):
        if self.currentPath.text():
            search = re.search("^\"(.*?)\"$", self.currentPath.text())
            if search:
                self.currentPath.setText(search.group(1))
                return
            path = os.path.abspath(self.currentPath.text())
            if os.path.isdir(path):
                self.fileList.set_root(path)
            elif os.path.isfile(path):
                self.fileList.set_root(os.path.dirname(path))
                if self.fileList.filter_path(path):
                    self.fileList.target = path
                    reconnect(self.fileList.fileModel.directoryLoaded, self.fileList.on_load_select, self.fileList.on_loaded)
                    self.fileList.select_path(path)
                else:
                    path = os.path.dirname(path)
            elif os.path.isdir(os.path.dirname(path)):
                self.fileList.set_root(os.path.dirname(path))

        else:
            self.fileList.set_root("")

    def set_root(self, path):
        self.fileList.set_root(path)

    def execute(self):
        if os.path.isfile(self.fileList.path):
            self.executed.emit(self.fileList.path)
        else:
            self.fileList.set_root(self.fileList.path)