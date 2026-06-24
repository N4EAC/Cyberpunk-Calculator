@echo off
setlocal
cd /d "%~dp0"
set PY=python
where py >nul 2>nul
if %errorlevel%==0 set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo Python 3 was not found. Install Python 3 from python.org, then run this again.
  pause
  exit /b 1
)
%PY% -m pip install --upgrade pip
%PY% -m pip install pyinstaller pillow
%PY% make_icon.py
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name "Cyberpunk Calc" --icon "cyberpunk_calc.ico" --add-data "cyberpunk_calc.ico;." cyberpunk_calc.py
if errorlevel 1 (
  echo.
  echo Build failed. Check the messages above.
  pause
  exit /b 1
)
echo.
echo Build complete.
echo EXE created here: %cd%\dist\Cyberpunk Calc.exe
pause
