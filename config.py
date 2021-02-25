import os
import json
import sys

import re

APP = re.findall("(\S*?)[\.\d]", os.path.basename(sys.executable))[0].upper()

ICON_PATH = os.path.normpath(os.path.join(__file__, "..", "icons")).replace("\\", "/")
SETTING_PATH = os.path.normpath(os.path.join(__file__, "..", "users", os.environ.get('USERNAME'))).replace("\\", "/")
PROJECT = os.environ.get("PROJECTNAME", "Project")

def get_settings():
    if os.path.isfile(SETTING_PATH+"/settings.json"):
        with open(SETTING_PATH+"/settings.json", "r") as setting_file: 
            settings = json.load(setting_file)
    else:
        settings = {
            'startup_show' : True,
            'close_on_open' : True,
            'new_window' : False,
        }
        save_settings(settings)
    return settings
        
def save_settings(settings):
    if not os.path.exists(SETTING_PATH):
        os.makedirs(SETTING_PATH)
    with open(SETTING_PATH + "/settings.json", "w") as setting_file: 
        setting_file.write(json.dumps(settings, indent = 4) ) 

def get_recent():
    if os.path.isfile(SETTING_PATH+"/recent.json"):
        with open(SETTING_PATH+"/recent.json", "r") as recent_file: 
            recent = json.load(recent_file)
    else:
        recent = {
            PROJECT : {
                "BLENDER" : [],
                "MAYA" : [],
                "NUKE" : []
            }
        }
        save_recent(recent)
    
    if recent.get(PROJECT, None) is None:
        recent.update({
            PROJECT : {
                "BLENDER" : [],
                "MAYA" : [],
                "NUKE" : []
            }
        })
    return recent

def save_recent(recent):
    if not os.path.exists(SETTING_PATH):
        os.makedirs(SETTING_PATH)
    with open(SETTING_PATH + "/recent.json", "w") as recent_file: 
        recent_file.write(json.dumps(recent, indent = 4) ) 