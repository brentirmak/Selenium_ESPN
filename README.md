<b>(8/1) Background:</b> <br> 
1) This is a shell script that runs a Selenium Python script 3 different times (consecutively) against the ESPN site using the Chrome, FireFox, Safari and Edge browsers. <br>
2) When a failure happens, a screenshot is captured and an email alert is generated. <br>
3) After each run, results are stored in a MySQL database. <br>
4) The shell script toggles set -e/set +e to abort if an issue occurs with storing the results in MySQL. Otherwise, if the ESPN monitoring portion of the script fails, the shell script execution proceeds to the next browser.<br> 
5) Visual Studio dev environment is on MacOS <br>
6) Jenkins Instance is running on Ubuntu 24.04 - Jenkins(1) <br>