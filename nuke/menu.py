from datetime import datetime
import sys
import os

main_folder = os.path.normpath(os.path.join(__file__, "..", ".."))
if not main_folder in sys.path:
    sys.path.append(main_folder)

from gui import WelcomeScreen
import gui
import config

ws = WelcomeScreen()
if ws.settings['startup_show']:
	ws.show()

import nuke

def addRecent():
	nkPath = nuke.Root().knob("name").value()
	if nkPath != "":
		recent = config.get_recent()
		data = next((data for data in recent[config.PROJECT][config.APP] if data["path"] == nkPath), None)
		if data:
			data["access_date"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		else:
			recent[config.PROJECT][config.APP].append({
				"path" : nkPath,
				"access_date" : datetime.now().strftime("%Y/%m/%d %H:%M:%S")
			})
		config.save_recent(recent)

nuke.addOnScriptLoad(addRecent)
nuke.addOnScriptSave(addRecent)

menu = nuke.menu('Nuke')
menu.addCommand( 'General/Welcome Screen', gui.show, 'ctrl+w' )