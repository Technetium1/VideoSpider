@echo off
TITLE VideoSpider Compiler
python -V > NUL 2> NUL
IF errorlevel 1 ECHO PYTHON NOT IN PATH! && PAUSE && EXIT
CD %~dp0
python -m pip install -U pyinstaller
pyinstaller -F -i web.ico --clean VideoSpider.py
MOVE /Y %~dp0dist\VideoSpider.exe %~dp0
RMDIR /S /Q build __pycache__ dist
DEL /F /S /Q VideoSpider.spec
ECHO Done! File is located in %~dp0
ECHO Keep VideoSpiderKeys.ini and VideoSpider.exe together!
PAUSE
EXIT
