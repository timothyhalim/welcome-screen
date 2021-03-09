import sys
import os

try:
    main_folder = os.path.normpath(os.path.join(__file__, "..", "..", "..", ".."))
except:
    import inspect
    main_folder = os.path.normpath(os.path.join(inspect.getframeinfo(inspect.currentframe()).filename, "..", "..", "..", ".."))
if not main_folder in sys.path:
    sys.path.append(main_folder)
    
### Import Required Modules ###
from WelcomeScreen.main import gui as wsgui
wsgui.show()