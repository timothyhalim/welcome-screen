import nuke
import config
from datetime import datetime

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

from gui import WelcomeScreen

ws = WelcomeScreen()
if ws.settings['startup_show']:
	ws.show()

menu = nuke.menu('Nuke')
menu.addCommand( 'General/Welcome Screen', ws.show, 'ctrl+w' )