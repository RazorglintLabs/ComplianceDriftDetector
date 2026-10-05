@echo off
cd /d "%~dp0"
python software\sale01_validation_console.py
if errorlevel 1 pause
