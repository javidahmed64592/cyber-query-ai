CyberQueryAI Installer README
=============================

Welcome to CyberQueryAI! This is an Ollama-powered web application designed to assist with cybersecurity tasks. The installer scripts provided in this package will set up the application on your system, including creating a virtual environment, installing dependencies, and configuring necessary files.

URL: https://github.com/javidahmed64592/cyber-query-ai

There are two installer scripts included:
- `install_cyber_query_ai.sh` for Linux and macOS systems
- `install_cyber_query_ai.bat` for Windows systems

Please run the appropriate script for your operating system. Below is a detailed step-by-step breakdown of what each script does.

Prerequisites
-------------
- Python 3.13 or higher must be installed on your system.
- The `uv` package manager must be available (it will be used for virtual environment and package management).
- For Linux/macOS: Bash shell and standard Unix tools (e.g., tput, chmod).
- For Windows: Command Prompt (cmd.exe) and Windows batch scripting support.
- Sufficient disk space for the virtual environment and application files.
- Administrative privileges may be required for service creation on Linux/macOS.

Ollama
------
By default, CyberQueryAI uses the `mistral` and `bge-m3` LLMs.
You'll need to ensure you `pull` whichever models you plan to use:

```
ollama pull mistral
ollama pull bge-m3
```

Which Script to Run?
--------------------
- If you are on Linux or macOS, run `./install_cyber_query_ai.sh`
- If you are on Windows, run `install_cyber_query_ai.bat` (double-click or run from Command Prompt)

Step-by-Step Breakdown: Linux/macOS Installer (install_cyber_query_ai.sh)
------------------------------------------------------------------------

1. **Setup Variables and Directories**:
   - Defines package name, virtual environment name, executable names, and file paths.
   - Creates a `service` directory for service-related scripts.

2. **Create Virtual Environment**:
   - Uses `uv venv` to create a new Python virtual environment named `.venv` in the current directory.
   - This isolates the application's dependencies from your system Python.

3. **Install from Wheel**:
   - Finds the CyberQueryAI wheel file (`.whl`) in the current directory.
   - Installs the package using `uv pip install`.
   - Removes the wheel file after installation to clean up.

4. **Extract Application Files**:
   - Locates the site-packages directory within the virtual environment.
   - Moves configuration and documentation files (`config.json`, `README.md`, `SECURITY.md`, `LICENSE`) from the installed package to the root installation directory.
   - This makes these files easily accessible for configuration and reference.

5. **Create API Executable**:
   - Generates a bash script named `cyber-query-ai` that sets the `CYBER_QUERY_AI_ROOT_DIR` environment variable and runs the main application.
   - Makes the script executable with `chmod +x`.

6. **Create Systemd Service**:
   - Creates a systemd service file (`cyber_query_ai.service`) in the `service` directory.
   - Configures the service to run the application as a background service, with automatic restarts on failure.
   - Sets up logging to `cyber_query_ai.log`.

7. **Create Service Management Scripts**:
   - `start_service.sh`: Copies the service file to `/etc/systemd/system`, enables and starts the service.
   - `stop_service.sh`: Stops the service and optionally disables/removes it.
   - Makes both scripts executable.

8. **Create Uninstall Script**:
   - Generates `uninstall_cyber_query_ai.sh` which removes all files in the current directory.
   - Makes the script executable.

9. **Cleanup**:
   - Removes the installer scripts (`install_cyber_query_ai.sh` and `install_cyber_query_ai.bat`) and this file.

10. **Display Success Message**:
   - Prints instructions on how to run the application, configure it, manage the service, view logs, and uninstall.

Step-by-Step Breakdown: Windows Installer (install_cyber_query_ai.bat)
-------------------------------------------------------------------

1. **Setup Variables**:
   - Defines package name, virtual environment name, executable names, and file paths.
   - Sets paths for the script directory, virtual environment, and binary directory.

2. **Create Virtual Environment**:
   - Uses `uv venv` to create a new Python virtual environment named `.venv` in the current directory.
   - This isolates the application's dependencies from your system Python.

3. **Install from Wheel**:
   - Finds the CyberQueryAI wheel file (`.whl`) in the current directory.
   - Installs the package using `uv pip install`.
   - Deletes the wheel file after installation to clean up.

4. **Extract Application Files**:
   - Locates the site-packages directory within the virtual environment.
   - Moves configuration and documentation files (`config.json`, `README.md`, `SECURITY.md`, `LICENSE`) from the installed package to the root installation directory.
   - This makes these files easily accessible for configuration and reference.

5. **Create Executable Launcher**:
   - Generates a batch script named `cyber-query-ai.bat` that:
     - Sets the `CYBER_QUERY_AI_ROOT_DIR` environment variable.
     - Starts Ollama server in the background.
     - Runs the main CyberQueryAI application.
     - Stops the Ollama server after the application exits.
   - This launcher ensures Ollama is running when the application starts.

6. **Display Success Message**:
   - Prints instructions on how to run the application, configure it, view logs, and uninstall.

7. **Cleanup**:
   - Deletes the installer scripts (`install_cyber_query_ai.bat` and `install_cyber_query_ai.sh`) and this file.

Post-Installation Instructions
------------------------------
- **Running the Application**:
  - Linux/macOS: Run `./cyber-query-ai` from the installation directory.
  - Windows: Run `cyber-query-ai.bat` from the installation directory.

- **Configuration**:
  - Edit `config.json` to customize the application's settings.

- **Service Management (Linux/macOS only)**:
  - To start as a system service: Run `./service/start_service.sh` (requires sudo).
  - To stop the service: Run `./service/stop_service.sh` (requires sudo).

- **Viewing Logs**:
  - Linux/macOS: Check `cyber_query_ai.log` or use `journalctl -u cyber_query_ai.service`.
  - Windows: Check `cyber_query_ai.log` in the installation directory.

- **Uninstallation**:
  - Linux/macOS: Run `./uninstall_cyber_query_ai.sh` to remove all files.
  - Windows: Simply delete the entire installation directory.

Important Notes
---------------
- The installer creates a virtual environment to avoid conflicts with your system Python.
- On Linux/macOS, the service runs under your current user account.
- The application requires Ollama to be installed and configured separately (the Windows installer starts Ollama automatically).
- If you encounter permission issues, run the installer with appropriate privileges (e.g., sudo on Linux/macOS).
- The installer modifies your system by creating service files (Linux/macOS) or starting background processes (Windows).
- Review the generated scripts and configuration files before running them in production.

For more information about CyberQueryAI, visit the project repository or consult the main README.md file.

If you have any questions or issues, please refer to the project's documentation or create an issue on GitHub.
