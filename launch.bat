@echo off
ECHO "Activating Virtual Environment. . ."
CALL venv\Scripts\activate.bat

ECHO.
ECHO Starting Dev Server. . .
ECHO Visit https://127.0.0.1:8000/ in your browser!
ECHO CTRL+C to stop server
ECHO.

python manage.py runserver

ECHO Server stopped.
pause
