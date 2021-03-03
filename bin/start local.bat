@echo off
call cd .. && ^
:loop
echo PLAFOSUS is starting... && ^
cmd /c "venv\Scripts\activate.bat & python manage.py runserver & deactivate &"
echo PLAFOSUS crashed. Restarting... && ^
timeout /T 60
goto loop
