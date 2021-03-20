import sys
import subprocess
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


def getDrives():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    argument = " ".join(["wmic", "logicaldisk", "get", "/format:csv"])
    drives = []
    result = subprocess.Popen(argument, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, universal_newlines=True)
    keys = None
    driveTypes = [
        "Unknown",
        "No Root Directory",
        "Removable Disk",
        "Local Disk",
        "Network Drive",
        "Compact Disc",
        "RAM Disk"
    ]
    for line in result.stdout.readlines():
        if line in ["", "\n"]: continue
        splits = line.split(",")
        if keys is None:
            keys = splits
        if splits != keys:
            letter = splits[keys.index("Caption")]
            driveType = splits[keys.index("DriveType")]
            drivePath = splits[keys.index("ProviderName")]
            driveName = splits[keys.index("VolumeName")]
            
            drive = QFileInfo(letter+"/")
            drive.driveType = driveTypes[int(driveType)]
            drive.driveName = drivePath if drivePath else driveName if driveName else driveTypes[int(driveType)]
            drives.append(drive)
    return drives

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

class SearchBar(QLineEdit):
    activated = Signal(bool)

    def __init__(self, parent=None, completerContents=[]):
        super(SearchBar, self).__init__(parent)

        self._completer = QCompleter(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self._completer)
        self.updateCompletionList(completerContents)
        self.completerActive = self._completer.popup().isVisible()

    def updateCompletionList(self, autocomplete_list):
        self.autocomplete_model = QStandardItemModel()
        for text in autocomplete_list:
            self.autocomplete_model.appendRow(QStandardItem(text))
        self._completer.setModel(self.autocomplete_model)

    def paintEvent(self, QPaintEvent):
        super(SearchBar, self).paintEvent(QPaintEvent)
        prev = self.completerActive
        self.completerActive = self._completer.popup().isVisible()
        if prev != self.completerActive:
            self.activated.emit(self.completerActive)

class FileModel(QAbstractTableModel):
    rootPathChanged = Signal(str, str)

    def __init__(self, root=""):
        super(FileModel, self).__init__()
        self._root = root
        self._qdir = QDir()
        self._qdir.setFilter(QDir.NoDot | QDir.Files | QDir.AllDirs)
        self._headers = ("Filename", "Size", "Type", "Modified")
        self._drives = getDrives()
        self._icons = QFileIconProvider()

        self.setRootPath(self._root)

    def indexFromFilePath(self, path):
        path = path + "/" if path.endswith(":") else path
        path = os.path.abspath(path).replace("\\", "/")
        for row in range(self.rowCount()):
            if self._data[row].absoluteFilePath() == path:
                return self.index(row, 0, QModelIndex())
        return self.index(0, 0, QModelIndex())

    def filePathFromIndex(self, index):
        row = index.row()
        return self._data[row].filePath()

    def rootPath(self):
        return self._root

    def setRootPath(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        if path == "" or os.path.isdir(path):
            prevRoot = self._qdir.path()
            self._data = []
            self.beginResetModel()
            self.endResetModel()
            if path:
                path = os.path.abspath(path)
                self._qdir.setPath(path)
                self._data = self._qdir.entryInfoList()
            else:
                self._qdir.setPath(path)
                self._data = self._drives
            self._root = path
            self.rootPathChanged.emit(self._qdir.path(), prevRoot)

    def setFilter(self, filter):
        self._qdir.setFilter(filter)

    def setNameFilters(self, filter):
        self._qdir.setNameFilters(filter)

    def headerData(self, section, orientation, role):
        if (orientation == Qt.Horizontal):
            if role == Qt.TextAlignmentRole:
                if section >= 1:
                    return int(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    return int(Qt.AlignLeft | Qt.AlignVCenter)
            elif role == Qt.DisplayRole:
                return self._headers[section]

        return super(FileModel, self).headerData(section, orientation, role=role)

    def data(self, index, role):
        row = index.row()
        column = index.column()
        data = self._data[row]
        if role == Qt.DisplayRole:
            if column == 0:
                if data.isRoot():
                    try:
                        return "{0}| {1}".format(data.absolutePath(), data.driveName)
                    except:
                        return "{0}| {1}".format(data.absolutePath(), "")
                if data.fileName():
                    return data.fileName()
                else:
                    return data.absolutePath()
            elif column == 1:
                if data.isFile():
                    factor = 1024
                    size = data.size()
                    for unit in ["", "K", "M", "G", "T", "P"]:
                        if size < factor:
                            return "{0:.2f}{1}B".format(size, unit)
                        size /= factor
            elif column == 2:
                if data.isRoot():
                    try:
                        return data.driveType
                    except:
                        pass
                return self._icons.type(data)
            elif column == 3:
                return data.lastModified()
        elif role == Qt.DecorationRole:
            if column == 0:
                return self._icons.icon(data)
        elif role == Qt.TextAlignmentRole:
            if column >= 1:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            else:
                return int(Qt.AlignLeft | Qt.AlignVCenter)

    def sort(self, column, order=Qt.AscendingOrder):
        #Todo
        return super(FileModel, self).sort(column, order=order)

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._headers)

    def getFiles(self):
        return [d.absoluteFilePath() for d in self._data]

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
        self.fileModel = FileModel()
        self.fileModel.setFilter(QDir.NoDot | QDir.Files | QDir.AllDirs)
        if self.filterExtension:
            self.fileModel.setNameFilters(self.filterExtension)
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

        self.set_root("")

    def isdrive(self, path):
        path.replace("\\", "/")
        drives = [d.filePath() for d in QDir.drives()]
        return path in drives

    def set_root(self, path):
        self.fileModel.setRootPath(path)

    def on_root_changed(self, newPath, oldPath):
        self.current_index = self.fileModel.index(0, 0)
        if newPath != oldPath:
            if newPath in oldPath or newPath == "":
                prevselection = [f for f in oldPath.replace(newPath, "").split("/") if f]
                if prevselection:
                    filepath = os.path.join(newPath, prevselection[0])
                    self.current_index = self.fileModel.indexFromFilePath(filepath)
            
        self.tableSelectionModel.setCurrentIndex(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.tableSelectionModel.select(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.scrollTo(self.current_index)

    def on_selection_changed(self, current, prev):
        self.path = self.fileModel.filePathFromIndex(current)
        self.pathChanged.emit(self.path)

    def on_double_click(self, index=None):
        if self.path.endswith("..") and self.isdrive(self.path.replace("..", "")):
            self.set_root("")
        elif os.path.isdir(self.path) or self.isdrive(self.path):
            self.set_root(self.path)
        elif os.path.isfile(self.path):
            self.executed.emit(self.path)

    def select_path(self, path):
        self.current_index = self.fileModel.indexFromFilePath(path)
        self.tableSelectionModel.setCurrentIndex(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.tableSelectionModel.select(self.current_index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.scrollTo(self.current_index)

    def get_files(self):
        return self.fileModel.getFiles()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.on_double_click()
                
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
        self.currentPath = SearchBar()
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

        # self.currentPath.activated.connect(self.on_completer_activated)
        self.currentPath.textChanged.connect(self.on_text_changed)
        self.currentPath.returnPressed.connect(self.validate_path)
        self.fileList.pathChanged.connect(self.on_path_changed)
        self.fileList.executed.connect(self.execute)
        self.exeButton.clicked.connect(self.execute)
        self.exeButton.setMinimumWidth(70)

        self.on_path_changed(self.fileList.path)

        self.currentPath.installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.FocusIn):
            print(source)
        if source is self.currentPath:
            if (event.type() == QEvent.FocusOut):
                reconnect(self.fileList.pathChanged, self.on_path_changed)
                self.validate_path()
            elif (event.type() == QEvent.FocusIn):
                reconnect(self.fileList.pathChanged)
        elif source is self.fileList:
            if (event.type() == QEvent.FocusOut):
                reconnect(self.currentPath.textChanged, self.on_text_changed)
            elif (event.type() == QEvent.FocusIn):
                reconnect(self.currentPath.textChanged)
        return super(FileBrowser, self).eventFilter(source, event)
    
    def validate_path(self):
        self.change_current_path(self.fileList.path)
        if os.path.isfile(self.fileList.path):
            self.execute()
        else:
            self.fileList.setFocus()
    
    # def on_completer_activated(self, value):
    #     if value:
    #         print("Activated")
    #         reconnect(self.currentPath.textChanged)
    #     else:
    #         print("Deactivated")
    #         print(self.currentPath.text())
    #         reconnect(self.currentPath.textChanged, self.on_text_changed)

    def change_current_path(self, text):
        reconnect(self.currentPath.textChanged)
        self.currentPath.setText(text)
        reconnect(self.currentPath.textChanged, self.on_text_changed)
        
    def on_path_changed(self, newpath):
        newpath = re.sub("(.*?)/(\.)+$", r"\1/", newpath)
        self.change_current_path(newpath)

    def on_text_changed(self):
        if self.currentPath.text():
            search = re.search("^\"(.*?)\"$", self.currentPath.text())
            if search:
                self.currentPath.setText(search.group(1))
                return

            path = self.currentPath.text()
            self.fileList.set_root(path)
            # files = self.fileList.get_files()
            # self.currentPath.updateCompletionList(files)

            if os.path.isfile(path):
                self.fileList.select_path(path)
        else:
            self.fileList.set_root("")

    def set_root(self, path):
        self.fileList.set_root(path)

    def execute(self):
        if os.path.isfile(self.fileList.path):
            self.executed.emit(self.fileList.path)
        else:
            self.fileList.set_root(self.fileList.path)
# try:
#     if __name__ == "__main__":
#         app=QApplication(sys.argv)
#         window=FileBrowser()
#         window.show()
#         app.exec_()

# except:
#     window=FileBrowser()
#     window.show()
