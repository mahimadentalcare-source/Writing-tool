@echo off
echo Check for Python Installation...
python --version
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check the box "Add Python to PATH" during installation.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Starting Dental Presentation Generator...
streamlit run app.py
pause
