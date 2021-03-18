try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
import os

class FileSystemModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(FileSystemModel, self).__init__(parent=parent)

    def fileInfo(self, index):
        return self.node(index).fileInfo()

    def index(self, row, column, parent=None):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QModelIndex()
        parent = self.node(parent) if self.indexValid(parent)  else self.root()

        i = self.translateVisibleLocation(parent, row)
        if i >= parent.visibleChildren.size():
            return QModelIndex()

        child = parent.visibleChildren.at(i)
        indexNode = parent.children.value(child)

        return self.createIndex(row, column, indexNode)

    def indexFromFilepath(self, path):
        node = self.node(path, False)
        return self.index(node)