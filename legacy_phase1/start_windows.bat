@echo off
setlocal
cd /d "%~dp0"
title NeuroLens Local Server

where py >nul 2>nul
if %errorlevel%==0 (
  echo Starting NeuroLens at http://localhost:8000
  start "" "http://localhost:8000"
  py -m http.server 8000
  goto :end
)

where python >nul 2>nul
if %errorlevel%==0 (
  echo Starting NeuroLens at http://localhost:8000
  start "" "http://localhost:8000"
  python -m http.server 8000
  goto :end
)

echo Python was not found. Opening the standalone application directly.
start "" "%~dp0index.html"
echo Install Python if you prefer to run the local web server.
pause

:end
endlocal
