@echo off
setlocal enabledelayedexpansion

REM === Setup Variables ===
set PACKAGE_NAME=cyber_query_ai
set VENV_NAME=.venv
set EXE_FILENAME=cyber-query-ai.bat
set CONFIG_FILENAME=config.json
set LOG_FILENAME=cyber_query_ai.log
set README_FILENAME=README.txt

set SCRIPT_DIR=%~dp0
set FULL_VENV_PATH=%SCRIPT_DIR%%VENV_NAME%
set BIN_DIR=%FULL_VENV_PATH%\Scripts

REM === Create virtual environment ===
echo Creating virtual environment...
uv venv %VENV_NAME%

REM === Install wheel ===
for %%f in (%PACKAGE_NAME%-*-py3-none-any.whl) do (
    echo Installing %%f...
    uv pip install "%%f"
    del "%%f"
)

REM === Create executable launcher ===
echo Creating launcher...
echo @echo off > "%SCRIPT_DIR%%EXE_FILENAME%"
echo set "CYBER_QUERY_AI_ROOT_DIR=%SCRIPT_DIR%" >> "%SCRIPT_DIR%%EXE_FILENAME%"
echo start "" /min cmd /c "ollama serve" >> "%SCRIPT_DIR%%EXE_FILENAME%"
echo echo Ollama server started... >> "%SCRIPT_DIR%%EXE_FILENAME%"
echo "%BIN_DIR%\cyber-query-ai.exe" %%* >> "%SCRIPT_DIR%%EXE_FILENAME%"
echo echo Stopping Ollama server... >> "%SCRIPT_DIR%%EXE_FILENAME%"
echo taskkill /f /im ollama.exe >nul 2>&1 >> "%SCRIPT_DIR%%EXE_FILENAME%"

REM === Create README ===
echo CyberQueryAI has been installed successfully. > "%SCRIPT_DIR%%README_FILENAME%"
echo Run the application using: "%EXE_FILENAME%" >> "%SCRIPT_DIR%%README_FILENAME%"
echo Configure the application by editing: "%CONFIG_FILENAME%" >> "%SCRIPT_DIR%%README_FILENAME%"
echo To view logs: type "%LOG_FILENAME%" >> "%SCRIPT_DIR%%README_FILENAME%"
echo To uninstall, delete the folder: "%SCRIPT_DIR%" >> "%SCRIPT_DIR%%README_FILENAME%"

REM === Display README ===
type "%SCRIPT_DIR%%README_FILENAME%"

REM === Self-delete installer ===
echo Installation complete. Cleaning up installer...
del /q "%~dp0install*"
