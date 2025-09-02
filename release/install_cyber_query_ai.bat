@echo off
setlocal enabledelayedexpansion

REM === Setup Variables ===
set PACKAGE_NAME=cyber_query_ai
set VENV_NAME=.venv
set EXE_FILENAME=cyber-query-ai.bat
set CONFIG_FILENAME=config.json
set LOG_FILENAME=cyber_query_ai.log

set INSTALLER_README_FILENAME=readme.txt
set CONFIG_FILENAME=config.json
set APP_README_FILENAME=README.md
set SECURITY_FILENAME=SECURITY.md
set LICENSE_FILENAME=LICENSE

set SCRIPT_DIR=%~dp0
set FULL_VENV_PATH=%SCRIPT_DIR%%VENV_NAME%
set BIN_DIR=%FULL_VENV_PATH%\Scripts
set SITE_PACKAGES_DIR=%FULL_VENV_PATH%\Lib\site-packages

REM === Prepare root directory ===
echo Preparing root directory...
move "%SITE_PACKAGES_DIR%%CONFIG_FILENAME%" "%SCRIPT_DIR%%CONFIG_FILENAME%"
move "%SITE_PACKAGES_DIR%%APP_README_FILENAME%" "%SCRIPT_DIR%%APP_README_FILENAME%"
move "%SITE_PACKAGES_DIR%%SECURITY_FILENAME%" "%SCRIPT_DIR%%SECURITY_FILENAME%"
move "%SITE_PACKAGES_DIR%%LICENSE_FILENAME%" "%SCRIPT_DIR%%LICENSE_FILENAME%"

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
echo CyberQueryAI has been installed successfully.
echo Run the application using: "%EXE_FILENAME%"
echo Configure the application by editing: "%CONFIG_FILENAME%"
echo To view logs: type "%LOG_FILENAME%"
echo To uninstall, delete the folder: "%SCRIPT_DIR%"

REM === Self-delete installer ===
echo Installation complete. Cleaning up installer...
del /q "%~dp0install*"
del /q "%SCRIPT_DIR%%INSTALLER_README_FILENAME%"
