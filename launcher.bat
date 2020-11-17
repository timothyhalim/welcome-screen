@echo off

SET curDir=

REM *** Project Environment ***
SET PROJECTNAME=Test
SET PROJECTCODE=TST


REM *** Nuke Path Environment ***
set PYTHONPATH=%PYTHONPATH%;
set NUKE_PATH=%NUKE_PATH%;%cd%

REM *** Software Licensing Environment ***
set foundry_LICENSE=4101@deployserver

REM *** Launch Nuke 9.0v5 ***
cmd /c start "" "C:\Program Files\Nuke9.0v5\Nuke9.0.exe"