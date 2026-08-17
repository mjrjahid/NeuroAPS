@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NeuroAPS Clinical Research Workspace

echo ============================================================
echo   NeuroAPS Clinical Research Workspace
echo ============================================================
echo.

rem Use the existing environment when it is already valid.
if exist ".venv\Scripts\python.exe" (
  set "VENV_PY=%CD%\.venv\Scripts\python.exe"
  goto :install_and_run
)

rem Find a normal Python installation without requiring Python in PATH.
set "PYTHON_EXE="
for %%P in (
  "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
  "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
  "%ProgramFiles%\Python313\python.exe"
  "%ProgramFiles%\Python312\python.exe"
  "%ProgramFiles%\Python311\python.exe"
  "%ProgramFiles%\Python310\python.exe"
) do (
  if not defined PYTHON_EXE if exist "%%~P" set "PYTHON_EXE=%%~P"
)

rem Fall back to the Python Launcher or a PATH installation when available.
if not defined PYTHON_EXE (
  for /f "delims=" %%P in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%P"
)
if not defined PYTHON_EXE (
  for /f "delims=" %%P in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%P"
)
if not defined PYTHON_EXE (
  for /f "delims=" %%P in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%P"
)

if not defined PYTHON_EXE goto :python_not_found

echo Found Python:
echo   %PYTHON_EXE%
"%PYTHON_EXE%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 goto :python_too_old

echo.
echo Creating the local environment...
"%PYTHON_EXE%" -m venv ".venv"
if errorlevel 1 goto :venv_error

set "VENV_PY=%CD%\.venv\Scripts\python.exe"
if not exist "%VENV_PY%" goto :venv_error

:install_and_run
echo.
echo Installing or checking required packages...
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 goto :package_error
"%VENV_PY%" -m pip install -r "requirements.txt"
if errorlevel 1 goto :package_error

echo.
echo Validating the knowledge base and sample registry...
"%VENV_PY%" "ingest.py"
if errorlevel 1 goto :validation_error
"%VENV_PY%" "scripts\build_sample_manifest.py"
if errorlevel 1 goto :validation_error

echo.
echo Starting the application at http://localhost:8501
echo Keep this window open while using the GUI.
echo Press Ctrl+C here to stop the application.
echo.
"%VENV_PY%" -m streamlit run "app.py"
if errorlevel 1 goto :application_error
goto :end

:python_not_found
echo.
echo ERROR: Python 3.10 or newer was not found.
echo.
echo This launcher checked the standard Windows installation folders,
echo the Python Launcher, and PATH. Install 64-bit Python from:
echo   https://www.python.org/downloads/windows/
echo.
echo During installation, enable "Add python.exe to PATH", then run
echo start_windows.bat again.
goto :failed

:python_too_old
echo.
echo ERROR: The detected Python is older than version 3.10.
echo Install Python 3.12 and run start_windows.bat again.
goto :failed

:venv_error
echo.
echo ERROR: The local .venv environment could not be created.
echo Confirm that the Python installer included the venv and pip components.
goto :failed

:package_error
echo.
echo ERROR: A required package could not be installed.
echo Check the internet connection and the messages shown above.
goto :failed

:validation_error
echo.
echo ERROR: The bundled knowledge base or sample registry did not validate.
echo Keep the extracted folder structure unchanged and try again.
goto :failed

:application_error
echo.
echo ERROR: Streamlit stopped unexpectedly. Review the messages shown above.
goto :failed

:failed
echo.
pause
exit /b 1

:end
endlocal
