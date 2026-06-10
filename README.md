<b>(6/9) Background:</b> <br> 
1) This is a shell script that runs a Selenium Python script 3 different times (consecutively) against the ESPN site using the Chrome, FireFox and Edge browsers. <br> 
2) After each run, results are stored in a MySQL database. <br>
3) The shell script toggles set -e/set +e to abort if an issue occurs with storing the results in MySQL. Otherwise, if the ESPN monitoring portion of the script fails, the shell script execution proceeds to the next browser.<br> 
4) PyCharm Dev Environment is on Ubuntu 26.04 - Jenkins(1) <br>
5) Jenkins Instance is running on Ubuntu 26.04 - Jenkins(1) <br>