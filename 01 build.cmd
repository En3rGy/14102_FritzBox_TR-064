@echo off
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib
@echo on

cd ..\..
C:\Python27\python generator.pyc "14102_FritzBox_TR-064" UTF-8

xcopy .\projects\14102_FritzBox_TR-064\src .\projects\14102_FritzBox_TR-064\release

@echo Fertig.

@pause