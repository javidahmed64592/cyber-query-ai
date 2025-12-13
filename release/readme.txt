CyberQueryAI Installer README
=============================

Welcome to CyberQueryAI! This is an Ollama-powered web application designed to assist with cybersecurity tasks. The installer scripts provided in this package will set up the application on your system, including creating a virtual environment, installing dependencies, and configuring necessary files.

URL: https://github.com/javidahmed64592/cyber-query-ai

This package includes the installer script `install_cyber_query_ai.sh` for Linux and macOS systems.

Below is a detailed step-by-step breakdown of what the installer does.

Prerequisites
-------------
- Python 3.13 or higher must be installed on your system.
- The `uv` package manager must be available (it will be used for virtual environment and package management).
- For Linux/macOS: Bash shell and standard Unix tools (e.g., tput, chmod).
- For Windows: Command Prompt (cmd.exe) and Windows batch scripting support.
- Sufficient disk space for the virtual environment and application files.

Ollama
------
By default, CyberQueryAI uses the `mistral` and `bge-m3` LLMs.
You'll need to ensure you `pull` whichever models you plan to use:

```
ollama pull mistral
ollama pull bge-m3
```

Running the Installer
---------------------
On Linux or macOS, run: `./install_cyber_query_ai.sh`

Step-by-Step Breakdown
----------------------

1. **Setup Variables and Directories**:
   - Defines package name, virtual environment name, executable names, and file paths.

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
   - Generates a bash script named `cyber-query-ai` that runs the main application.
   - Makes the script executable with `chmod +x`.

6. **Create Uninstall Script**:
   - Generates `uninstall_cyber_query_ai.sh` which removes the virtual environment and all files in the installation directory.
   - Makes the script executable.

7. **Generate SSL Certificate**:
   - Creates self-signed SSL certificate files (`cert.pem` and `key.pem`) in the `certs/` directory.
   - Uses the configuration from `configuration/config.json`.

8. **Display Success Message**:
   - Prints instructions on how to run the application, configure it, view logs, and uninstall.

9. **Cleanup**:
   - Removes the installer script and this readme file.

Post-Installation Instructions
------------------------------
- **Running the Application**:
  - Run `./cyber-query-ai` from the installation directory.

- **Configuration**:
  - Edit `configuration/config.json` to customize the application's settings (host, port, LLM model, embedding model).

- **Uninstallation**:
  - Run `./uninstall_cyber_query_ai.sh` to remove the virtual environment and all installation files.

Important Notes
---------------
- The installer creates a virtual environment to isolate the application from your system Python.
- Ollama must be installed and running separately before starting the application.
- Ensure you've pulled the required models (`ollama pull mistral && ollama pull bge-m3`).
- SSL certificates are auto-generated for HTTPS support; consider using proper certificates in production.
- If you encounter permission issues, ensure the installer script is executable (`chmod +x install_cyber_query_ai.sh`).

For more information about CyberQueryAI, visit the project repository or consult the main README.md file.

If you have any questions or issues, please refer to the project's documentation or create an issue on GitHub.
