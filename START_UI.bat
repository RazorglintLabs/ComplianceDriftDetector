@echo off
cd /d "%~dp0"
python software\ui_app.py
if errorlevel 1 pause
