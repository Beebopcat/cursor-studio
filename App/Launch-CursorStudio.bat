@echo off
rem Cursor Studio launcher - runs the dark-mode installer with the PowerShell built into Windows 11.
powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File "%~dp0CursorStudio.ps1"
