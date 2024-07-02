@echo off
:: Batch script to run mg_track.py script as administrator
cd /d %~dp0
powershell -Command "& { Start-Process python -ArgumentList 'mg_track.py' -Verb RunAs }"
