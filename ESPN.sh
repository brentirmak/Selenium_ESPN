#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CALLED_FROM="$(pwd)"

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

PYTHON_EXECUTABLE="${PYTHON_EXECUTABLE:-python3}"
echo "Python executable: $PYTHON_EXECUTABLE"

# Optional browser argument.
#
# Examples:
#   ./ESPN.sh
#   ./ESPN.sh Safari
#
# If a browser is supplied, only that browser is executed.
# If no browser is supplied, Chrome, Firefox and Edge are executed.
REQUESTED_BROWSER="${1:-}"

OVERALL_STATUS=0

run_browser_test() {
    local browser="$1"

    echo ""
    echo "============================================================"
    echo "Starting ${browser} browser test"
    echo "============================================================"

    echo "Running the script for the ${browser} driver/browser"

    if "$PYTHON_EXECUTABLE" ESPN.py --browser "$browser"; then
        echo "[SUCCESS] ${browser} Selenium test completed successfully."
    else
        echo "[ERROR] ${browser} Selenium test FAILED."
        OVERALL_STATUS=1
    fi

    echo ""
    echo "Storing the results for the ${browser} driver/browser script run"

    if "$PYTHON_EXECUTABLE" ESPN_StoreDB.py; then
        echo "[SUCCESS] ${browser} results stored successfully."
    else
        echo "[ERROR] ${browser} results could NOT be stored."
        OVERALL_STATUS=1
    fi

    echo ""
    echo "Results have been stored - removing txt results file"
    rm -f Selenium_ESPN.txt

    sleep 5

    echo ""
    echo "Finished ${browser} browser test"
    echo "============================================================"
}


# ============================================================
# Requested single-browser execution
# ============================================================

if [ -n "$REQUESTED_BROWSER" ]; then

    echo ""
    echo "Single browser execution requested: $REQUESTED_BROWSER"

    case "$REQUESTED_BROWSER" in
        Chrome|Firefox|Edge|Safari)
            run_browser_test "$REQUESTED_BROWSER"
            ;;
        *)
            echo "[ERROR] Unsupported browser: $REQUESTED_BROWSER"
            echo "Supported browsers: Chrome, Firefox, Edge, Safari"
            exit 1
            ;;
    esac

else

    # ========================================================
    # Default execution
    #
    # Ubuntu/Linux:
    #   Chrome
    #   Firefox
    #   Edge
    #
    # Safari is handled by the separate macOS Jenkins job.
    # ========================================================

    run_browser_test "Chrome"
    run_browser_test "Firefox"
    run_browser_test "Edge"

fi


echo ""
echo "============================================================"

if [ "$OVERALL_STATUS" -eq 0 ]; then
    echo "ALL REQUESTED BROWSER TESTS COMPLETED SUCCESSFULLY"
else
    echo "ONE OR MORE REQUESTED BROWSER TESTS FAILED"
    echo "Review the Jenkins console output for the failed browser(s)."
fi

echo "============================================================"

exit "$OVERALL_STATUS"