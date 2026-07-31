#!/bin/bash

# Get directory where script is located
SCRIPT_DIR=$(dirname "$0")

# Get absolute path of script directory
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Get directory where script was called FROM
CALLED_FROM=$(pwd)

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

echo "Running the script for the Chrome driver/browser"
python3 ESPN.py --browser Chrome
set -e
echo "Storing the results for the Chrome driver/browser script run"
python3 ESPN_StoreDB.py
set +e
echo "Results have been stored - will remove txt results file"
rm Selenium_ESPN.txt

sleep 5

echo "Running the script for the Firefox driver/browser"
python3 ESPN.py --browser Firefox
set -e
echo "Storing the results for the Firefox driver/browser script run"
python3 ESPN_StoreDB.py
set +e
echo "Results have been stored - will remove txt results file"
rm Selenium_ESPN.txt

sleep 5

echo "Running the script for the Edge driver/browser"
python3 ESPN.py --browser Edge
set -e
echo "Storing the results for the Edge driver/browser script run"
python3 ESPN_StoreDB.py
set +e
echo "Results have been stored - will remove txt results file"
rm Selenium_ESPN.txt

sleep 5

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "Running the script for the Safari driver/browser"
  python3 ESPN.py --browser Safari
  set -e
  echo "Storing the results for the Safari driver/browser script run"
  python3 ESPN_StoreDB.py
  set +e
  echo "Results have been stored - will remove txt results file"
  rm Selenium_ESPN.txt
else
  echo "Skipping Safari driver/browser script - not running on macOS"
fi

exit