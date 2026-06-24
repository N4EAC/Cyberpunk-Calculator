@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 cyberpunk_calc.py
  goto :done
)
where python >nul 2>nul
if %errorlevel%==0 (
  python cyberpunk_calc.py
  goto :done
)
echo Python was not found. Install Python 3 from python.org, then run this again.
pause
:done
