import sys
import os
from maya import cmds, mel
import maya.OpenMaya as om

### Add to Sys Path ###
try:
    main_folder = os.path.normpath(os.path.join(__file__, "..", "..", "..", ".."))
except:
    import inspect
    main_folder = os.path.normpath(os.path.join(inspect.getframeinfo(inspect.currentframe()).filename, "..", "..", "..", ".."))
    
if not main_folder in sys.path:
    sys.path.append(main_folder)

### Import Required Modules ###
from WelcomeScreen.main import gui as wsgui
from WelcomeScreen.main import config as wsconfig
reload(wsgui)
reload(wsconfig)

### Registering Callback ###
def store_recent(*args, **kwargs):
    wsconfig.add_recent( cmds.file(sn=True, q=True) )

def registerCallbacks():
    referencesCallback = [
        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, store_recent),
        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, store_recent)
    ]
    print("WelcomeScreen Callback Registered")
    return referencesCallback
    
def unregisterCallbacks(referencesCallback):
    for cb in referencesCallback:
        om.MMessage.removeCallback(cb)

try:
    if welcomescreencallback:
        print("Already Initialized")
        pass
except:
    welcomescreencallback = registerCallbacks()
        
### Registering HotKey ###
name = "WelcomeScreen"
annotation = "Welcome Screen Show"
command = "from WelcomeScreen.main import gui as wsgui; wsgui.show()"

try:
    if welcomescreeninitialized:
        print("Already Registered")
        pass
except:
    # if cmds.runTimeCommand(name, q=True, exists=True):
        # cmds.runTimeCommand(name, e=True, delete=True)
    if not cmds.runTimeCommand(name, q=True, exists=True):
        cmds.runTimeCommand(
                name,
                annotation=annotation,
                command=command,
                commandLanguage="python",
                category="Custom Scripts"
            )
            
        cmds.nameCommand(
                "{0}NameCommand".format(name),
                annotation=annotation,
                command=name
            )
        
    if cmds.hotkeySet(q=True, current=True) == "Maya_Default":
        if not cmds.hotkeySet("Custom", q=True, exists=True):
            cmds.hotkeySet("Custom", current=True)
        else:
            cmds.hotkeySet("Custom", edit=True, current=True)
            
        cmds.hotkey (
                keyShortcut = "w",
                ctl = True,
                sht = True,
                name = "{0}NameCommand".format(name)
            )

    ### Register Menu ###
    MainMayaWindow = mel.eval('$tmpVar=$gMainWindow')
    if cmds.menu('MayaWindow|Welcome_Screen', q=True, ex=True):
        cmds.deleteUI(cmds.menu('MayaWindow|Welcome_Screen', e=1, dai=True))

    customMenu = cmds.menu('Welcome Screen', parent=MainMayaWindow)
    mn = mel.eval('''menuItem -label "Welcome Screen Show" -command {0} -parent "MayaWindow|Welcome_Screen" show'''.format(name) )
    
    welcomescreeninitialized = True

### Start Up Show ###
if wsconfig.get_settings()['startup_show']:
	wsgui.start()
