import sys
import os
import nuke

### Add to Sys Path ###
main_folder = os.path.normpath(os.path.join(__file__, "..", "..", "..", ".."))
nuke.tprint("Welcome Screen:", main_folder)
if not main_folder in sys.path:
    sys.path.append(main_folder)

### Import Required Modules ###
from WelcomeScreen.main import gui as wsgui
from WelcomeScreen.main import config as wsconfig

### Registering Callback ###
def store_recent():
    wsconfig.add_recent(nuke.Root().knob("name").value())
    
nuke.addOnScriptLoad(store_recent)
nuke.addOnScriptSave(store_recent)

### Registering Menu ###
menu = nuke.menu('Nuke')
menu.addCommand( 'General/Welcome Screen', wsgui.show, 'ctrl+shift+w' )

### Start Up Show ###
ws = wsgui.WelcomeScreen()
if ws.settings['startup_show']:
	ws.show()
