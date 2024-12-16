@echo off
rem Define the log file path
set LOG_FILE=D:\Medic\MediGo\ProgramLog.log

rem Open ProgramLog.log in Notepad (optional, can be removed if not needed)
start notepad.exe "%LOG_FILE%"

rem Wait for Notepad to open (adjust the time if necessary)
timeout /t 2

rem Trim the log file to the last 10,000 lines using PowerShell
powershell -Command "Get-Content '%LOG_FILE%' | Select-Object -Last 10000 | Set-Content '%LOG_FILE%'"

rem Close Notepad
taskkill /f /im notepad.exe
