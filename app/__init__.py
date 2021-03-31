import os
import sys
import re

# GLOBAL VARIABLE
APP = re.findall("(\S*?)[\.\d]", os.path.basename(sys.executable))[0].upper()
# APP command
try:
    exec("from .{0} import command".format(APP.lower()))
except:
    from .other import command