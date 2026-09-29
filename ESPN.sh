#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CALLED_FROM="$(pwd)"

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

PYTHON_EXECUTABLE="${PYTHON_EXECUTABLE:-python3}"
echo "Python executable: $PYTHON_EXECUTABLE"

# ------------------------------------------------------------
# JUnit reporting
#
# The Jenkins wrapper script exports JUNIT_REPORT (absolute path).
# When ESPN.sh is run by hand, fall back to ./reports/junit.xml.
# ------------------------------------------------------------
JUNIT_PATH="${JUNIT_REPORT:-${SCRIPT_DIR}/reports/junit.xml}"
REPORT_DIR="$(dirname "$JUNIT_PATH")"
mkdir -p "$REPORT_DIR"

# Parallel arrays holding one entry per test case.
T_BROWSER=()
T_NAME=()
T_STATUS=()
T_TIME=()
T_LOG=()

record_result() {
    # $1 browser, $2 test name, $3 exit code, $4 seconds, $5 log file
    T_BROWSER+=("$1")
    T_NAME+=("$2")
    T_STATUS+=("$3")
    T_TIME+=("$4")
    T_LOG+=("$5")
}

xml_escape() {
    # Escape XML special characters and strip control characters
    # (keeps tab and newline).
    sed -e 's/&/\&amp;/g' \
        -e 's/</\&lt;/g' \
        -e 's/>/\&gt;/g' \
        -e 's/"/\&quot;/g' \
    | tr -d '\000-\010\013-\037'
}

write_junit() {
    local total="${#T_NAME[@]}"
    local failures=0
    local total_time=0
    local i

    for i in "${!T_NAME[@]}"; do
        if [ "${T_STATUS[$i]}" -ne 0 ]; then
            failures=$((failures + 1))
        fi
        total_time=$((total_time + T_TIME[i]))
    done

    {
        echo '<?xml version="1.0" encoding="UTF-8"?>'
        echo "<testsuite name=\"Selenium_ESPN\" tests=\"${total}\" failures=\"${failures}\" errors=\"0\" skipped=\"0\" time=\"${total_time}\">"

        for i in "${!T_NAME[@]}"; do
            echo "  <testcase classname=\"Selenium_ESPN.${T_BROWSER[$i]}\" name=\"${T_NAME[$i]}\" time=\"${T_TIME[$i]}\">"

            if [ "${T_STATUS[$i]}" -ne 0 ]; then
                echo "    <failure message=\"Exit code ${T_STATUS[$i]}\">"
                if [ -f "${T_LOG[$i]}" ]; then
                    tail -n 40 "${T_LOG[$i]}" | xml_escape
                fi
                echo "    </failure>"
            fi

            echo "  </testcase>"
        done

        echo "</testsuite>"
    } > "$JUNIT_PATH"

    echo "JUnit report written to: $JUNIT_PATH"
}

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
    local start rc
    local test_log="${REPORT_DIR}/espn_${browser}.log"
    local store_log="${REPORT_DIR}/store_${browser}.log"

    echo ""
    echo "============================================================"
    echo "Starting ${browser} browser test"
    echo "============================================================"

    echo "Running the script for the ${browser} driver/browser"

    start=$SECONDS

    "$PYTHON_EXECUTABLE" -u ESPN.py --browser "$browser" 2>&1 | tee "$test_log"
    rc=${PIPESTATUS[0]}

    if [ "$rc" -eq 0 ]; then
        echo "[SUCCESS] ${browser} Selenium test completed successfully."
    else
        echo "[ERROR] ${browser} Selenium test FAILED."
        OVERALL_STATUS=1
    fi

    record_result "$browser" "ESPN test" "$rc" "$((SECONDS - start))" "$test_log"

    echo ""
    echo "Storing the results for the ${browser} driver/browser script run"

    start=$SECONDS

    "$PYTHON_EXECUTABLE" -u ESPN_StoreDB.py 2>&1 | tee "$store_log"
    rc=${PIPESTATUS[0]}

    if [ "$rc" -eq 0 ]; then
        echo "[SUCCESS] ${browser} results stored successfully."
    else
        echo "[ERROR] ${browser} results could NOT be stored."
        OVERALL_STATUS=1
    fi

    record_result "$browser" "Store results" "$rc" "$((SECONDS - start))" "$store_log"

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


write_junit

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