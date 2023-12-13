
@echo off

rem Change directory to your virtual environment directory (replace 'venv' with your actual directory)
cd mytrainenv

rem Activate the virtual environment (replace 'Scripts' with 'bin' for Linux/macOS)
call Scripts\activate

rem Change directory to the root directory of your Django project
cd ..
cd mytrain


start http://127.0.0.1:5000/

rem Run the Django development server
python wsgi.py

