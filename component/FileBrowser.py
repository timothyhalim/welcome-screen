# TODO 

import subprocess
import sys
import os
import re
from glob import glob

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

def getDrives():
    platform = sys.platform
    if platform.startswith("win"):
        drives = []
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
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        argument = " ".join(["wmic", "logicaldisk", "get", "/format:csv"])
        result = subprocess.Popen(
                    argument, 
                    stdout=subprocess.PIPE, 
                    stdin=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    startupinfo=startupinfo, 
                    universal_newlines=True
                )

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
    elif platform.startswith("linux"):
        drives = QDir.drives()
    elif platform == "darwin":
        drives = QDir.drives()
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

class PathBar(QLineEdit):
    upPressed = Signal()
    downPressed = Signal()

    def __init__(self, parent=None):
        super(PathBar, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.upPressed.emit()
        elif event.key() == Qt.Key_Down:
            self.downPressed.emit()
        else:
            super(PathBar, self).keyPressEvent(event)

class FileModel(QAbstractTableModel):
    rootPathChanged = Signal(str, str)

    def __init__(self, root=""):
        super(FileModel, self).__init__()

        self._qdir = QDir()
        self._qdir.setFilter(QDir.NoDot | QDir.Files | QDir.AllDirs)
        self._headers = ("Filename", "Size", "Type", "Modified")
        self._icons = QFileIconProvider()

        self._qdir.setPath(root)
        self.refresh()
        self.rootPathChanged.emit(root, "")

    def rowFromFilePath(self, path):
        path = path + "/" if path.endswith(":") else path
        path = os.path.abspath(path).replace("\\", "/")
        # Search for case sensitive first
        for row in range(self.rowCount()):
            if self._data[row].absoluteFilePath() == path:
                return row
        # Search for case insensitive
        for row in range(self.rowCount()):
            if self._data[row].absoluteFilePath().lower() == path.lower():
                return row
        return 0

    def filePathFromIndex(self, index):
        row = index.row()
        return self._data[row].filePath()

    def rootPath(self):
        return self._qdir.path()

    def fixCase(self, path):
        unc, p = os.path.splitdrive(path)
        unc = unc.upper() if ":" in unc else unc
        r = glob(unc + re.sub(r'([^:/\\])(?=[/\\]|$)', r'[\1]', p))
        return r and r[0] or path

    def setRootPath(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        if path == "" or os.path.isdir(path):
            prevRoot = self.rootPath()
            if path:
                if re.search("[a-zA-Z]:/\.\.$", path):
                    path = ""
                else:
                    if path.endswith(":"):
                        path += "/"
                    path = os.path.abspath(path).replace("\\", "/")
                path = self.fixCase(path)
            if path != self.rootPath():
                self._data = []
                self.beginResetModel()
                self._qdir.setPath(path)
                self._data = self._qdir.entryInfoList() if path else self._drives
                backPath = os.path.join(self.rootPath(), "..").replace("\\", "/")
                if not backPath in [d.filePath() for d in self._data] and self.rootPath() != "":
                    self._data.insert(0, QFileInfo(backPath))
                self.endResetModel()
                self.rootPathChanged.emit(self.rootPath(), prevRoot)

    def refresh(self):
        self._drives = getDrives()
        self._qdir.refresh()
        self.beginResetModel()
        self.endResetModel()
        self._data = self._qdir.entryInfoList() if self.rootPath() else self._drives

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
                        return "{0} ({1})".format(data.driveName, data.absolutePath())
                    except:
                        return data.absolutePath()
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
                            return "{0:.2f} {1}B".format(size, unit)
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
                if data.filePath().endswith("/..") and data.isDir():
                    return QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogBack))
                return self._icons.icon(data)
        elif role == Qt.TextAlignmentRole:
            if column >= 1:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            else:
                return int(Qt.AlignLeft | Qt.AlignVCenter)

    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        if col == 0:
            if self.rootPath():
                self._data = sorted(self._data, key=lambda x : x.fileName())
            else:
                self._data = sorted(self._data, key=lambda x : x.absolutePath())
        elif col == 1:
            self._data = sorted(self._data, key=lambda x : x.size())
        elif col == 2:
            if self.rootPath():
                self._data = sorted(self._data, key=lambda x : self._icons.type(x))
            else:
                self._data = sorted(self._data, key=lambda x : x.driveType)
        elif col == 3:
            self._data = sorted(self._data, key=lambda x : x.lastModified())
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._headers)

    def getFiles(self):
        return [d.absoluteFilePath() for d in self._data]

class FileList(QTableView):
    pathSelected = Signal(str)
    rootChanged = Signal(str)
    executed = Signal(str)

    def __init__(self, parent=None, filterExtension=[]):
        super(FileList, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.path = ""
        self.prev = ""
        self.target = ""
        self.filterExtension = filterExtension

        # Model
        self.fileModel = FileModel()
        self.fileModel.setFilter(QDir.NoDot | QDir.Files | QDir.AllDirs)
        if self.filterExtension:
            self.fileModel.setNameFilters(self.filterExtension)
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
        self.setColumnWidth(3,150)
        
        # Signal
        self.fileModel.rootPathChanged.connect(self.onRootChanged)
        self.tableSelectionModel.currentChanged.connect(self.onSelectionChanged)
        self.doubleClicked.connect(self.onDoubleClick)

        self.setRoot("")
        self.fileModel.rootPathChanged.emit("", "")

    def isdrive(self, path):
        path = path.replace("\\", "/")
        drives = [d.filePath().lower() for d in QDir.drives()]
        return path.lower() in drives

    def root(self):
        return self.fileModel.rootPath()

    def setRoot(self, path):
        self.fileModel.setRootPath(path)

    def onRootChanged(self, newPath, oldPath):
        index = self.fileModel.index(0, 0)
        filepath = self.fileModel.filePathFromIndex(index)
        if newPath != oldPath:
            if newPath in oldPath or newPath == "":
                prevselection = [f for f in oldPath.replace(newPath, "").split("/") if f]
                if prevselection:
                    filepath = os.path.join(newPath, prevselection[0])
        self.selectPath(filepath)
        self.rootChanged.emit(newPath)

    def onSelectionChanged(self, current, prev):
        self.path = self.fileModel.filePathFromIndex(current)
        self.pathSelected.emit(self.path)

    def onDoubleClick(self, index=None):
        self.execute()

    def execute(self):
        if self.path.endswith("..") and self.isdrive(self.path.replace("..", "")):
            self.setRoot("")
        elif os.path.isdir(self.path) or self.isdrive(self.path):
            self.setRoot(self.path)
        elif os.path.isfile(self.path):
            self.executed.emit(self.path)

    def selectPath(self, path):
        self.selectRow(self.fileModel.rowFromFilePath(path))

    def selectIndex(self, index):
        self.tableSelectionModel.setCurrentIndex(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.tableSelectionModel.select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        self.scrollTo(index)

    def selectRow(self, row):
        row = max(row, 0)
        row = min(row, self.fileModel.rowCount()-1)
        index = self.fileModel.index(row, 0)
        self.selectIndex(index)

    def selectPrev(self):
        currentRow = self.currentIndex().row()
        self.selectRow(currentRow-1)

    def selectNext(self):
        currentRow = self.currentIndex().row()
        self.selectRow(currentRow+1)

    def getFiles(self):
        return self.fileModel.getFiles()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.execute()
                
        elif event.key() == Qt.Key_Backspace:
            if self.fileModel.rootPath():
                root = os.path.abspath(self.fileModel.rootPath())
                paths = [d for d in root.split("\\") if d]
                if len(paths) > 1:
                    parentdir = "/".join(paths+[".."])
                else:
                    parentdir = ""

                self.setRoot(parentdir)

        elif event.key() == Qt.Key_F5:
            index = self.currentIndex()
            self.fileModel.refresh()
            self.selectIndex(index)

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
            super(FileList, self).keyPressEvent(event)
        
class FileBrowser(QWidget):
    executed = Signal(str)
    def __init__(self, parent=None, filterExtension=[], exeLabel="Open", title="Open File"):
        QWidget.__init__(self, parent=None)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.fileList = FileList(filterExtension=filterExtension)

        self.fileLayout = QHBoxLayout()
        self.currentPath = PathBar()
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

        self.currentPath.textChanged.connect(self.onTextChanged)
        self.currentPath.returnPressed.connect(self.execute)
        self.currentPath.upPressed.connect(self.selectPrev)
        self.currentPath.downPressed.connect(self.selectNext)
        self.fileList.rootChanged.connect(self.onRootChanged)
        self.fileList.pathSelected.connect(self.onPathChanged)
        self.fileList.executed.connect(self.execute)
        self.exeButton.clicked.connect(self.execute)
        self.exeButton.setMinimumWidth(70)

        self.onPathChanged(self.fileList.path)

        self.currentPath.installEventFilter(self)
        self.fileList.installEventFilter(self)
        self.exeButton.installEventFilter(self)
        
        self.lastFocus = None

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusOut:
            if source != self.lastFocus :
                self.lastFocus = source
        if source is self.currentPath:
            if (event.type() == QEvent.FocusOut):
                reconnect(self.fileList.pathSelected, self.onPathChanged)
                self.validatePath()
            elif (event.type() == QEvent.FocusIn):
                reconnect(self.fileList.pathSelected)
        elif source is self.fileList:
            if (event.type() == QEvent.FocusOut):
                reconnect(self.currentPath.textChanged, self.onTextChanged)
            elif (event.type() == QEvent.FocusIn):
                reconnect(self.currentPath.textChanged)
        return super(FileBrowser, self).eventFilter(source, event)
    
    def validatePath(self):
        self.changeCurrentPath(self.fileList.path)

    def onRootChanged(self):
        root = self.fileList.root()
        currentText = self.currentPath.text()
        self.changeCurrentPath(root+currentText[len(root):])

    def cleanupPath(self, path):
        search = re.search("^\"(.*?)\"$", path)
        if search:
            path = search.group(1)
        
        search = re.search("(.*?)\.\.$", path)
        if search:
            path = search.group(1)

        path = path.replace("\\", "/")

        return path

    def changeCurrentPath(self, path):
        reconnect(self.currentPath.textChanged)
        path = self.cleanupPath(path)
        self.currentPath.setText(path)
        reconnect(self.currentPath.textChanged, self.onTextChanged)
        
    def onPathChanged(self, path):
        path = self.cleanupPath(path)
        self.changeCurrentPath(path)

    def onTextChanged(self):
        if self.currentPath.text():
            cp = self.currentPath.text()
            if re.search("^\"(.*?)\"$", cp) or re.search("(.*?)\.\.$", cp):
                self.currentPath.setText(self.cleanupPath(cp))
                            
            splits = cp.split("/")
            path = "/".join(splits[:-1]) if len(splits) > 1 else cp + "/"
            self.setRoot(path)

            files = [f.lower() for f in self.files]
            for file in files:
                if cp.lower() in file:
                    self.selectPath(file)
                    break
        else:
            self.setRoot("")
    
    def selectPrev(self):
        self.fileList.selectPrev()
        self.changeCurrentPath(self.fileList.path)

    def selectNext(self):
        self.fileList.selectNext()
        self.changeCurrentPath(self.fileList.path)

    def selectPath(self, path):
        self.fileList.selectPath(path)

    def setRoot(self, path):
        if path != self.fileList.root():
            self.fileList.setRoot(path)
            self.files = self.fileList.getFiles()

    def execute(self):
        if os.path.isfile(self.fileList.path):
            self.executed.emit(self.fileList.path)
        else:
            self.setRoot(self.fileList.path)
        self.changeCurrentPath(self.fileList.path)