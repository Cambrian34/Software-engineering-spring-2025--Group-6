@echo off
echo Starting setup...

:: Run pyenv install script
call pyenv_install.bat
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

:: Run pyenv local script
call pyenv_local.bat
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

:: Run setup venv script
@echo off
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.

echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated.

echo Installing requirements...
pip install -r requirements.txt
echo Requirements were installed.

echo    Setup complete! Run "venv\Scripts\activate" to activate the environment.
echo    (Note: Run this and following command without quotation marks.)

echo       After virtual environment is activated, run "cd fetchandfind"
echo       Then run "python manage.py runserver" to run the project.
echo          Hold "ctrl" and then click on the server URL to open the webapp.
echo          Hold "ctrl" and then press "c" to stop the server.
