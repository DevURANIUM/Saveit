@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET SCRIPT_DIR=%~dp0
CD /D "%SCRIPT_DIR%"


python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip.
    pause
    exit /b 1
)

IF NOT EXIST ".env" (
    echo Creating .env file based on .env.example...
    copy ".env.example" ".env" >nul

    set /p API_ID="Enter your API_ID: "
    set /p API_HASH="Enter your API_HASH: "
    set /p HANDLER="Enter your HANDLER (e.g., .saveit): "

    powershell -Command "(gc .env) -replace 'API_ID=.*','API_ID=%API_ID%' | Out-File -encoding ASCII .env"
    powershell -Command "(gc .env) -replace 'API_HASH=.*','API_HASH=%API_HASH%' | Out-File -encoding ASCII .env"
    powershell -Command "(gc .env) -replace 'HANDLER=.*','HANDLER=%HANDLER%' | Out-File -encoding ASCII .env"
)

pip show telethon >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Telethon is already installed. Updating...
    pip install --upgrade telethon
) ELSE (
    echo Installing Telethon...
    pip install telethon
)

echo Running Saveit.py...
python Saveit.py

echo Done.
pause

