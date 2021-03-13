from maya import cmds
try:
    from PySide2.QtWidgets import QApplication
except:
    from PySide.QtGui import QApplication

def get_app_window():
    for w in QApplication.topLevelWidgets():
        if w.objectName() == 'MayaWindow':
            return w

def check():
    ok = False
    if cmds.file(q=True, modified=True):
        confirm = cmds.confirmDialog( 
            title='Continue', 
            message='File is not saved continue?', 
            button=['Yes', 'Cancel'], 
            defaultButton='Yes', 
            cancelButton='Cancel', 
            dismissString='Cancel' 
        ) 
        ok = (confirm == 'Yes')
    return ok

def clear_scene():
    if check():
        cmds.file(new=True, f=True)

def open_file(filepath = "", new_window = False):
    if filepath == "":
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        result = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, okc="Open", fileMode=1)
        if result:
            filepath = result[0]
        else:
            return
        
    if get_open_file() and get_open_file() != filepath:
        if not new_window:
            # clear_scene()
            cmds.file(filepath, o=True, f=True)
        else:
            if check():
                cmds.file(filepath, o=True, f=True)
    else:
        try:
            cmds.file(filepath, o=True, f=True)
        except:
            pass

def new_scene(new_window = False):
    if not new_window:
        clear_scene()
    else:
        clear_scene()

def get_open_file():
    return cmds.file(sn=True, q=True)