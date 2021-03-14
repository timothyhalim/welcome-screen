try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
import os

from sys import platform as _platform

# if _platform == "linux" or _platform == "linux2": # linux
# elif _platform == "darwin": # MAC OS X
# elif _platform == "win32": # Windows
# elif _platform == "win64": # Windows 64-bit
iconProvider = QFileIconProvider()

def drives():
    result = []
    for drive in QDir.drives():
        d = drive.absoluteFilePath()
        d = os.path.abspath(d)
        if not d in result:
            result.append(d)
    return result

def getFileList(path):
    result = []
    if path:
        fullpath = os.path.abspath(path)
        try:
            if os.path.isdir(fullpath):
                for f in os.listdir(fullpath):
                    try:
                        path = os.path.abspath(os.path.join(fullpath, f))
                        result.append(FileInfo(path))
                    except:
                        pass
        except:
            pass
    else:
        for d in drives():
            try:
                result.append(FileInfo(d))
            except:
                pass
    return result

class FileInfo(QFileInfo):
    def __init__(self, path, parent=None):
        super(FileInfo, self).__init__(path)
        # self.filePath = os.path.abspath(path)
        # self.baseName = os.path.basename(self.filePath) 
        # self.dir = os.path.dirname(self.filePath)
        self.icon = iconProvider.icon(self.filePath())

        self._childFetched = False
    

    # def get_info(self):
    #     self.isDir = os.path.isdir(self.filePath)
    #     self.isFile = os.path.isfile(self.filePath)
    #     self.isDrive = self.filePath in drives()
    #     self.size = os.path.getsize(self.filePath)
    #     self.lastModified = os.path.getmtime(self.filePath)
    #     self.createdTime = os.path.getctime(self.filePath)

    #     self.parent = None if self.isDrive else os.path.dirname(self.filePath) 

    def __repr__(self):
        return (self.filePath())

    def __str__(self):
        print (self.filePath())

    def reload(self):
        self.get_info()
        if self._childFetched:
            self.get_child()

    def get_child(self): 
        if self._childFetched :
            self.get_child()
        return self._child

    def set_child(self, value): 
        if self.isFile:
            self._child = None  
        else:
            self._child = []  
            for c in os.listdir(self.filePath):
                cf = FileInfo(os.path.join(self.filePath, c))
                self._child.append(cf)
        self._childFetched = True
    child = property(get_child, set_child)

class FileItemModel(QAbstractItemModel):
    def __init__(self, parent=None, root="", *args):
        super(FileItemModel, self).__init__(parent=parent, *args)
        self.root = root
        self.items = getFileList(root)
        # self.items = []
        self.header = ["Name", "Size", "Type", "Date"]

    def clearItem(self):
        self.items = []

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def addItem(self, item, at=None):
        if isinstance(item, FileInfo):
            if at is None:
                at = len(self.items)
            self.items.insert(at, item)
        else:
            raise Exception(item, "not instance of", FileInfo)

    def itemFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.itemFromIndex(child)
       
        if node is None:
            return QModelIndex()

        # parent = node.parent
           
        # if parent is None:
        #     return QModelIndex()
       
        # grandparent = parent.parent
        # if grandparent is None:
        #     return QModelIndex()
        # row = grandparent.rowOfChild(parent)
       
        # assert row != - 1
        # return self.createIndex(row, 0, parent)

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.items[row])

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        else:
            if index.column() == 0:
                return self.items[index.row()].baseName()
            elif index.column() == 1:
                return self.items[index.row()].size()
            elif index.column() == 2:
                return self.items[index.row()].suffix()
            elif index.column() == 3:
                return self.items[index.row()].lastModified()
            else:
                return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]

    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        if col == 0:
            self.items = sorted(self.items, key=lambda x : x.baseName())
        elif col == 1:
            self.items = sorted(self.items, key=lambda x : x.size())
        elif col == 2:
            self.items = sorted(self.items, key=lambda x : x.suffix())
        elif col == 3:
            self.items = sorted(self.items, key=lambda x : x.lastModified())
        if order == Qt.DescendingOrder:
            self.items.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class MyTableView(QTableView):
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent=parent)
        self.filemodel = FileItemModel(self)
        self.setModel(self.filemodel)
        self.setSortingEnabled(True)
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

# app = QApplication([])
# win = MyTableView()
# win.show()
# app.exec_()

