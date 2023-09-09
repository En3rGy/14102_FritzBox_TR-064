@echo off
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

echo ^<head^> > .\release\DE-log14102.html
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\DE-log14102.html
echo ^<title^>Logik - Fritz TR-064 (14102)^</title^> >> .\release\DE-log14102.html
echo ^<style^> >> .\release\DE-log14102.html
echo body { background: none; } >> .\release\DE-log14102.html
echo ^</style^> >> .\release\DE-log14102.html
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\DE-log14102.html
echo ^</head^> >> .\release\DE-log14102.html

@echo on

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\DE-log14102.html


cd ..\..
C:\Python27\python generator.pyc "14102_FritzBox_TR-064" UTF-8

xcopy .\projects\14102_FritzBox_TR-064\src .\projects\14102_FritzBox_TR-064\release /exclude:.\projects\14102_FritzBox_TR-064\src\exclude.txt

@echo Fertig.

@pause