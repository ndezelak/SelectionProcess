pyi-makespec --onefile --debug all  --hidden-import=six --console app.py
pause
pyinstaller app.spec
pause