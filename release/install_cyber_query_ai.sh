#!/bin/bash
set -eu

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

PACKAGE_NAME="cyber_query_ai"
WD=$(pwd)
VENV_NAME=".venv"
EXE_NAME="cyber-query-ai"
LOG_FILE="cyber_query_ai.log"
SERVICE_FILE="cyber_query_ai.service"
CREATE_SERVICE_FILE="start_service.sh"
STOP_SERVICE_FILE="stop_service.sh"
UNINSTALL_FILE="uninstall_cyber_query_ai.sh"
README_FILE="README.txt"

SERVICE_DIR="${WD}/service"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

EXE_PATH="${WD}/${EXE_NAME}"
LOG_PATH="${WD}/${LOG_FILE}"
SERVICE_PATH="${SERVICE_DIR}/${SERVICE_FILE}"
CREATE_SERVICE_PATH="${SERVICE_DIR}/${CREATE_SERVICE_FILE}"
STOP_SERVICE_PATH="${SERVICE_DIR}/${STOP_SERVICE_FILE}"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"
README_PATH="${WD}/${README_FILE}"

mkdir -p "${SERVICE_DIR}"

echo ${SEPARATOR}
echo "Creating virtual environment..."
uv venv ${VENV_NAME}

echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "${PACKAGE_NAME}-*-py3-none-any.whl")
uv pip install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "Creating API executable..."
cat > "${EXE_PATH}" << EOF
#!/bin/bash
export CYBER_QUERY_AI_ROOT_DIR=${WD}
${BIN_DIR}/${EXE_NAME} "\$@"
EOF
chmod +x "${EXE_PATH}"

echo "Creating service..."
cat > "${SERVICE_PATH}" << EOF
[Unit]
Description=Cyber Query AI Service
After=network.target
StartLimitBurst=5
StartLimitIntervalSec=60s

[Service]
Type=simple
User=${USER}
ExecStart=${EXE_PATH}
Restart=on-failure
RestartSec=5s
StandardOutput=append:${LOG_PATH}
StandardError=append:${LOG_PATH}

ProtectSystem=full
ReadWriteDirectories=${WD}
ReadWriteDirectories=${FULL_VENV_PATH}
ReadWriteDirectories=${LOGS_DIR}

[Install]
WantedBy=multi-user.target
EOF

echo "Creating service creation script..."
cat > "${CREATE_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

if [ ! -f /etc/systemd/system/${SERVICE_FILE} ]; then
    echo "Creating service..."
    sudo cp ${SERVICE_PATH} /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_FILE}
fi

echo "Starting service..."
sudo systemctl start ${SERVICE_FILE}
sudo systemctl status ${SERVICE_FILE}
EOF
chmod +x "${CREATE_SERVICE_PATH}"

echo "Creating service stop script..."
cat > "${STOP_SERVICE_PATH}" << EOF
#!/bin/bash
set -eu

echo "Stopping service..."
sudo systemctl stop ${SERVICE_FILE}

read -p "Disable service? (y/n): " disable_service
if [ "\$disable_service" == "y" ]; then
    echo "Disabling service..."
    sudo systemctl disable ${SERVICE_FILE}
    sudo systemctl daemon-reload
    sudo rm -f /etc/systemd/system/${SERVICE_FILE}
fi

EOF
chmod +x "${STOP_SERVICE_PATH}"

echo "Creating uninstall script..."
cat > "${UNINSTALL_PATH}" << EOF
#!/bin/bash
set -eu
cd "${WD}"
rm -rf *
EOF
chmod +x "${UNINSTALL_PATH}"

cat > "${README_PATH}" << EOF
Cyber Query AI has been installed successfully.
Run the application using: './${EXE_NAME}'

To create a start-up service for the Cyber Query AI, run: './service/${CREATE_SERVICE_FILE}'
To stop the service, run: './service/${STOP_SERVICE_FILE}'

To view the logs: 'cat ${LOG_FILE}'

To uninstall, run: './${UNINSTALL_FILE}'
EOF

echo "${SEPARATOR}"
cat "${README_PATH}"
echo "${SEPARATOR}"

rm -- "$0"
