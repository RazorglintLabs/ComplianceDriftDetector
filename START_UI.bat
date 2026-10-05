@echo off
cd /d "%~dp0"
python software\ui_app_sale01.py
if errorlevel 1 pause
