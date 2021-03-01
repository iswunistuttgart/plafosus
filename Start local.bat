@echo off
:loop
echo App is starting...
cmd /c "venv\Scripts\activate.bat & python manage.py runserver & deactivate &"
echo App crashed. Restarting...
timeout /T 1
goto loop
