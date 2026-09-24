#!/bin/bash

# ============================================================
# Selenium_ESPN Browser Test Runner
# ============================================================

# Stop immediately if an unexpected command fails.
set -e

# ------------------------------------------------------------
# Get directory where this script is located
# ------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Get directory where script was called from
CALLED_FROM="$(pwd)"

echo "============================================================"
echo " Selenium_ESPN Browser Test Runner"
echo "============================================================"
echo ""
echo "Script lives in: ${SCRIPT_DIR}"
echo "Called from:     ${CALLED_FROM}"
echo ""

# ------------------------------------------------------------
# Python Interpreter
# ------------------------------------------------------------
#
# Jenkins exports PYTHON_EXECUTABLE and points it to:
#
# /var/lib/jenkins/workspace/Selenium_ESPN/.venv/bin/python
#
# Using this explicitly prevents the system Python from being
# used accidentally.
# ------------------------------------------------------------

if [ -z "${PYTHON_EXECUTABLE}" ]; then
    echo "[WARNING] PYTHON_EXECUTABLE is not defined."
    echo "[WARNING] Falling back to python3."
    PYTHON_EXECUTABLE="python3"
fi

echo "Python executable: ${PYTHON_EXECUTABLE}"
echo ""

if [ ! -x "${PYTHON_EXECUTABLE}" ] && [ "${PYTHON_EXECUTABLE}" != "python3" ]; then
    echo "[ERROR] Python executable was not found or is not executable:"
    echo "${PYTHON_EXECUTABLE}"
    exit 1
fi

echo "Python version:"
"${PYTHON_EXECUTABLE}" --version
echo ""

# ------------------------------------------------------------
# Function: Run Browser Test
# ------------------------------------------------------------

run_browser_test() {

    BROWSER="$1"

    echo ""
    echo "============================================================"
    echo " Running ${BROWSER} Selenium Test"
    echo "============================================================"

    echo ""
    echo "Running the script for the ${BROWSER} driver/browser"

    "${PYTHON_EXECUTABLE}" "${SCRIPT_DIR}/ESPN.py" --browser "${BROWSER}"

    echo ""
    echo "Storing the results for the ${BROWSER} driver/browser script run"

    "${PYTHON_EXECUTABLE}" "${SCRIPT_DIR}/ESPN_StoreDB.py"

    echo ""
    echo "Results have been stored - will remove txt results file"

    if [ -f "${SCRIPT_DIR}/Selenium_ESPN.txt" ]; then
        rm -f "${SCRIPT_DIR}/Selenium_ESPN.txt"
        echo "[INFO] Selenium_ESPN.txt removed."
    else
        echo "[WARNING] Selenium_ESPN.txt was not found."
    fi

    echo ""
    echo "[SUCCESS] ${BROWSER} browser test completed."

    sleep 5
}

# ------------------------------------------------------------
# Chrome
# ------------------------------------------------------------

run_browser_test "Chrome"

# ------------------------------------------------------------
# Firefox
# ------------------------------------------------------------

run_browser_test "Firefox"

# ------------------------------------------------------------
# Edge
# ------------------------------------------------------------

run_browser_test "Edge"

# ------------------------------------------------------------
# Safari
# ------------------------------------------------------------

if [[ "$(uname -s)" == "Darwin" ]]; then

    run_browser_test "Safari"

else

    echo ""
    echo "============================================================"
    echo " Safari"
    echo "============================================================"
    echo ""
    echo "Skipping Safari driver/browser script - not running on macOS"
    echo ""

fi

# ------------------------------------------------------------
# Complete
# ------------------------------------------------------------

echo ""
echo "============================================================"
echo " Selenium_ESPN Browser Tests Complete"
echo "============================================================"

exit 0
```
