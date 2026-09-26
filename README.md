<b>(9/26) Background:</b> <br> 
<b>1)</b> This is a shell script that runs a Selenium Python script 3 different times (consecutively) against the ESPN site using the Chrome, FireFox, Safari and Edge browsers. <br>
<b>2)</b> When a failure happens, a screenshot is captured and an email alert is generated. <br>
<b>3)</b> After each run, results are stored in a MySQL database. <br>
<b>4)</b> The shell script toggles set -e/set +e to abort if an issue occurs with storing the results in MySQL. Otherwise, if the ESPN monitoring portion of the script fails, the shell script execution proceeds to the next browser.<br> 
<b>5)</b> Visual Studio dev environment is on MacOS <br>
<b>6)</b> Jenkins Instance is running on Ubuntu 24.04 - Jenkins(1) <br>