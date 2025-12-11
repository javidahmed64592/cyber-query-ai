#!/bin/bash
set -eu

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

PACKAGE_NAME="cyber_query_ai"
WD=$(pwd)
VENV_NAME=".venv"
EXE_NAME="cyber-query-ai"
LOG_FILE="cyber_query_ai.log"
UNINSTALL_FILE="uninstall_cyber_query_ai.sh"

INSTALLER_README_FILE="readme.txt"
CONFIG_FILE="config.json"
APP_README_FILE="README.md"
SECURITY_FILE="SECURITY.md"
LICENSE_FILE="LICENSE"

CONFIG_DIR="${WD}/configuration"
LOGS_DIR="${WD}/logs"
FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

CONFIG_PATH="${CONFIG_DIR}/${CONFIG_FILE}"
EXE_PATH="${WD}/${EXE_NAME}"
LOG_PATH="${LOGS_DIR}/${LOG_FILE}"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"

INSTALLER_README_PATH="${WD}/${INSTALLER_README_FILE}"
APP_README_PATH="${WD}/${APP_README_FILE}"
SECURITY_PATH="${WD}/${SECURITY_FILE}"
LICENSE_PATH="${WD}/${LICENSE_FILE}"

echo "Creating virtual environment..."
uv venv ${VENV_NAME}

echo "${SEPARATOR}"
echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "${PACKAGE_NAME}-*-py3-none-any.whl")
uv pip install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "${SEPARATOR}"
echo "Preparing root directory..."
mkdir -p "${CONFIG_DIR}"
mkdir -p "${LOGS_DIR}"

SITE_PACKAGES_DIR=$(find "${FULL_VENV_PATH}/lib" -name "site-packages" -type d | head -1)
mv "${SITE_PACKAGES_DIR}/configuration/${CONFIG_FILE}" "${CONFIG_PATH}"
mv "${SITE_PACKAGES_DIR}/${APP_README_FILE}" "${APP_README_PATH}"
mv "${SITE_PACKAGES_DIR}/${SECURITY_FILE}" "${SECURITY_PATH}"
mv "${SITE_PACKAGES_DIR}/${LICENSE_FILE}" "${LICENSE_PATH}"
mv "${SITE_PACKAGES_DIR}/.here" ".here"

echo "Creating API executable: ${EXE_PATH}"
cat > "${EXE_PATH}" << EOF
#!/bin/bash
export CYBER_QUERY_AI_ROOT_DIR=${WD}
${BIN_DIR}/${EXE_NAME} "\$@"
EOF
chmod +x "${EXE_PATH}"

echo "Creating uninstall script: ${UNINSTALL_PATH}"
cat > "${UNINSTALL_PATH}" << EOF
#!/bin/bash
set -eu
cd "${WD}"
rm -rf ${VENV_NAME}
rm -rf *
EOF
chmod +x "${UNINSTALL_PATH}"

echo "${SEPARATOR}"
echo "Generating self-signed SSL certificate..."
${BIN_DIR}/generate-certificate --config="${CONFIG_PATH}"

echo "${SEPARATOR}"
echo "CyberQueryAI has been installed successfully."
echo "Run the application using: './${EXE_NAME}'"
echo "Configure the application by editing: ${CONFIG_PATH}"
echo "To view the logs: 'cat ${LOG_FILE}'"
echo "To uninstall, run: './${UNINSTALL_FILE}'"
echo "${SEPARATOR}"

rm -f install*
rm -f "${INSTALLER_README_PATH}"
