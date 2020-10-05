@echo off
:loop
echo EOPP is starting...
cmd /c "venv\Scripts\activate.bat & python manage.py runserver & deactivate &"
echo EOPP crashed. Restarting...
timeout /T 1
goto loop
