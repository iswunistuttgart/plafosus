@echo off
echo Install virtualenv. && ^
call pip install virtualenv && ^
echo Create virtual environment 'venv'. && ^
call virtualenv venv && ^
echo Activate virtual environment. && ^
call venv\Scripts\activate.bat && ^
echo Install requirements. && ^
call venv\Scripts\pip install -r requirements.txt && ^
call venv\Scripts\deactivate.bat && ^
echo Installation successfully finished. && ^
pause