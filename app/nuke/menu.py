import sys
import os
import nuke

### Add to Sys Path ###
main_folder = os.path.normpath(os.path.join(__file__, "..", "..", "..", ".."))
if not main_folder in sys.path:
    sys.path.append(main_folder)

### Registering Callback ###
moduleName = os.path.basename(os.path.normpath(os.path.join(__file__, "..", "..", "..")))
exec("from {} import config as wsconfig".format(moduleName))

def store_recent():
    wsconfig.add_recent(nuke.Root().knob("name").value())
    
nuke.addOnScriptLoad(store_recent)
nuke.addOnScriptSave(store_recent)

if nuke.env['NukeVersionMajor'] < 10:
    execfile(os.path.join(main_folder, moduleName, "main.py"))
    
    ### Import Required Modules ###
    def wsgui_start():
        ws = WelcomeScreen()
        ws.start()

    ### Registering Menu ###
    menu = nuke.menu('Nuke')
    menu.addCommand( 'General/Welcome Screen', lambda f=wsgui_start : nuke.executeInMainThread(f), 'ctrl+shift+w' )

    ### Start Up Show ###
    if wsconfig.get_settings()['startup_show']:
        nuke.executeInMainThread(wsgui_start)

else:
    ### Import Required Modules ###
    exec("from {} import main as wsgui".format(moduleName))

    ### Registering Menu ###
    menu = nuke.menu('Nuke')
    menu.addCommand( 'General/Welcome Screen', lambda f=wsgui.start : nuke.executeInMainThread(f), 'ctrl+shift+w' )

    ### Start Up Show ###
    if wsconfig.get_settings()['startup_show']:
        nuke.executeInMainThread(wsgui.start)
