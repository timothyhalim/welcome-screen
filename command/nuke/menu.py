from datetime import datetime
import sys
import os
import nuke

main_folder = os.path.normpath(os.path.join(__file__, "..", "..", "..", ".."))
nuke.tprint("Welcome Screen:", main_folder)
if not main_folder in sys.path:
    sys.path.append(main_folder)

from WelcomeScreen import gui as wsgui
from WelcomeScreen import config as wsconfig

ws = wsgui.WelcomeScreen()
if ws.settings['startup_show']:
	ws.show()


def addRecent():
	nkPath = nuke.Root().knob("name").value()
	if nkPath != "":
		recent = wsconfig.get_recent()
		data = next((data for data in recent[wsconfig.PROJECT][wsconfig.APP] if data["path"] == nkPath), None)
		if data:
			data["access_date"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		else:
			recent[wsconfig.PROJECT][wsconfig.APP].append({
				"path" : nkPath,
				"access_date" : datetime.now().strftime("%Y/%m/%d %H:%M:%S")
			})
		wsconfig.save_recent(recent)

nuke.addOnScriptLoad(addRecent)
nuke.addOnScriptSave(addRecent)

menu = nuke.menu('Nuke')
menu.addCommand( 'General/Welcome Screen', wsgui.show, 'ctrl+w' )