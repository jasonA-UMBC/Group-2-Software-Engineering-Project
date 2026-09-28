@echo off

REM ---
REM setup_env.bat
REM Usage: setup_env.bat YOUR_API_KEY
REM Creates a .env file containing your API key 
REM Adds .env file to .gitignore
REM Run from root folder of project
REM ---

set "API_Key=%1"

if "%API_Key%"=="" (
    echo Please provide your API key as an argument.
    echo Usage: setup_env.bat YOUR_API_KEY
    exit /b 1
)

> ".env" (
    echo API_KEY=%API_Key%
)

