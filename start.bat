@echo off
REM Quick start script for Windows

echo ========================================
echo AI Market Analyst Agent - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your Gemini API key!
    echo    Open .env and replace 'your_gemini_api_key_here' with your actual key
    echo.
    pause
)

REM Run installation test
echo Running installation test...
python test_installation.py
echo.

echo ========================================
echo Setup complete!
echo.
echo To start the application:
echo 1. Backend: uvicorn src.main:app --reload
echo 2. Frontend: streamlit run app.py
echo.
echo Or use Docker: docker-compose up --build
echo ========================================
pause
