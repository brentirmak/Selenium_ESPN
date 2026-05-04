#!/bin/bash

# Get directory where script is located
SCRIPT_DIR=$(dirname "$0")

# Get absolute path of script directory
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Get directory where script was called FROM
CALLED_FROM=$(pwd)

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

jenkins_flag=false

if [[ "$SCRIPT_DIR" == *"/var/lib/jenkins"* ]]; then
  echo "It's running from Jenkins"
  jenkins_flag=true
else
  echo "It's running outside of Jenkins"
fi

echo "Running the script for the Chrome driver/browser"
python3 ESPN.py --browser Chrome
if jenkins_flag=false; then
  echo "Storing the results for the Chrome driver/browser script run"
  python3 ESPN_StoreDB.py
fi
echo "Results have been stored - will remove txt results file"
rm ESPN.txt
sleep 5
echo "Running the script for the Firefox driver/browser"
python3 ESPN.py --browser Firefox
if jenkins_flag=false; then
  echo "Storing the results for the Firefox driver/browser script run"
  python3 ESPN_StoreDB.py
fi
echo "Results have been stored - will remove txt results file"
rm ESPN.txt
sleep 5
echo "Running the script for the Edge driver/browser"
python3 ESPN.py --browser Edge
if jenkins_flag=false; then
  echo "Storing the results for the Edge driver/browser script run"
  python3 ESPN_StoreDB.py
fi
echo "Results have been stored - will remove txt results file"
rm ESPN.txt
exit