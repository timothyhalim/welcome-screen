#
#
#  Timothy Halim Septianjaya
#  timo.ink
#
#

import os
import nuke
import nukescripts

# SET TOOLS PATH
fileDirectory = os.path.dirname(__file__)

# RETURN EVERYTHING IN DIRECTORY AND CHECK FOR THE DIRECTORY ONLY
onlyDir = [ f for f in os.listdir( fileDirectory ) if os.path.isdir( os.path.join( fileDirectory, f ))]
for eachDir in onlyDir:
	#ADD THE DIRECTORY AS PLUGIN
    print("Adding Plugin : %s " %os.path.join(fileDirectory,eachDir))
    nuke.pluginAddPath( eachDir )

