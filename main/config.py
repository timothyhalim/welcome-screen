import os
import json
import sys
import re
from datetime import datetime

# FOR STABILITY USE PySide2
# add PySide2 and Shiboken to path
# try:
#     import PySide2
#     print("Using PySide2", PySide2.__version__)
# except:
#     lib = os.path.normpath(os.path.join(__file__, "..", "..", "venv", "Lib", "python27"))
#     if not lib in sys.path:
#         sys.path.append(lib)

APP = re.findall("(\S*?)[\.\d]", os.path.basename(sys.executable))[0].upper()

ICON_PATH = os.path.normpath(os.path.join(__file__, "..", "icons")).replace("\\", "/")
SETTING_PATH = os.environ.get('USERPROFILE', None)
if SETTING_PATH is None:
    SETTING_PATH = os.path.normpath(os.path.join(__file__, "..", "..", "users", os.environ.get('USERNAME', 'Anonymus'))).replace("\\", "/")
else:
    SETTING_PATH = os.path.join(SETTING_PATH, "Documents")
PROJECT = os.environ.get("PROJECTNAME", "Project")

def get_settings():
    if os.path.isfile(SETTING_PATH+"/welcomescreen_settings.json"):
        with open(SETTING_PATH+"/welcomescreen_settings.json", "r") as setting_file: 
            settings = json.load(setting_file)
    else:
        settings = {
            'startup_show' : True,
            'close_on_open' : True,
            'new_window' : False,
            'full_screen' : False,
        }
        save_settings(settings)
    return settings
        
def save_settings(settings):
    if not os.path.exists(SETTING_PATH):
        os.makedirs(SETTING_PATH)
    with open(SETTING_PATH + "/welcomescreen_settings.json", "w") as setting_file: 
        setting_file.write(json.dumps(settings, indent = 4) ) 

def get_recent():
    if os.path.isfile(SETTING_PATH+"/welcomescreen_recent.json"):
        with open(SETTING_PATH+"/welcomescreen_recent.json", "r") as recent_file: 
            recent = json.load(recent_file)
    else:
        recent = {
            PROJECT : {
                APP : []
            }
        }
        save_recent(recent)
    
    if (recent.get(PROJECT, None) is None) or (recent[PROJECT].get(APP, None) is None):
        recent.update({
            PROJECT : {
                APP : []
            }
        })
    return recent

def save_recent(recent):
    if not os.path.exists(SETTING_PATH):
        os.makedirs(SETTING_PATH)
    with open(SETTING_PATH + "/welcomescreen_recent.json", "w") as recent_file: 
        recent_file.write(json.dumps(recent, indent = 4) ) 
        
def add_recent(workfile):
    if workfile != "":
        print("Storing", workfile)
        recent = get_recent()
        data = next((data for data in recent[PROJECT][APP] if data["path"] == workfile), None)
        if data:
            data["access_date"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        else:
            recent[PROJECT][APP].append({
                "path" : workfile,
                "access_date" : datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            })
        save_recent(recent)