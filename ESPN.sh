#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CALLED_FROM="$(pwd)"

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

PYTHON_EXECUTABLE="${PYTHON_EXECUTABLE:-python3}"
echo "Python executable: $PYTHON_EXECUTABLE"

# Track whether any browser failed.
OVERALL_STATUS=0


run_browser_test() {
    local browser="$1"

    echo ""
    echo "============================================================"
    echo "Starting ${browser} browser test"
    echo "============================================================"

    # ---------------------------------------------------------
    # Run the Selenium test
    # ---------------------------------------------------------
    echo "Running the script for the ${browser} driver/browser"

    if "$PYTHON_EXECUTABLE" ESPN.py --browser "$browser"; then
        echo "[SUCCESS] ${browser} Selenium test completed successfully."
    else
        echo "[ERROR] ${browser} Selenium test FAILED."
        OVERALL_STATUS=1
    fi


    # ---------------------------------------------------------
    # Store the results in MySQL
    # ---------------------------------------------------------
    #
    # Run this independently even if ESPN.py failed.
    # This allows ESPN_StoreDB.py to store whatever results
    # were successfully written before the failure.
    #
    echo ""
    echo "Storing the results for the ${browser} driver/browser script run"

    if "$PYTHON_EXECUTABLE" ESPN_StoreDB.py; then
        echo "[SUCCESS] ${browser} results stored successfully."
    else
        echo "[ERROR] ${browser} results could NOT be stored."
        OVERALL_STATUS=1
    fi


    # ---------------------------------------------------------
    # Remove local results file
    # ---------------------------------------------------------
    echo ""
    echo "Results have been stored - removing txt results file"

    rm -f Selenium_ESPN.txt


    # ---------------------------------------------------------
    # Small delay before starting the next browser
    # ---------------------------------------------------------
    sleep 5

    echo ""
    echo "Finished ${browser} browser test"
    echo "============================================================"
}


# =============================================================
# Chrome
# =============================================================
run_browser_test "Chrome"


# =============================================================
# Firefox
# =============================================================
run_browser_test "Firefox"


# =============================================================
# Edge
# =============================================================
run_browser_test "Edge"


# =============================================================
# Safari
# =============================================================
if [[ "$(uname -s)" == "Darwin" ]]; then
    run_browser_test "Safari"
else
    echo ""
    echo "Skipping Safari driver/browser script - not running on macOS"
fi


# =============================================================
# Final Jenkins status
# =============================================================

echo ""
echo "============================================================"

if [[ "$OVERALL_STATUS" -eq 0 ]]; then
    echo "ALL BROWSER TESTS COMPLETED SUCCESSFULLY"
else
    echo "ONE OR MORE BROWSER TESTS FAILED"
    echo "Review the Jenkins console output for the failed browser(s)."
fi

echo "============================================================"

exit "$OVERALL_STATUS"
