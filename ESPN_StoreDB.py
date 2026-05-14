import os
import sys
import mysql.connector
import time
import pytz
from datetime import datetime

import ESPN_Parameters

espn_results_file = ESPN_Parameters.espn_test_parameters['RESULTS_FILE']
test_folder_path = ESPN_Parameters.espn_test_parameters['TEST_FOLDER_PATH']
test_name = ESPN_Parameters.espn_test_parameters['TEST_NAME']
run_type = "manual"

errors = []

# File to store overall Heartbeat test information locally - also used for DB storing purposes
if "var/lib/jenkins/workspace" in os.getcwd():
    print("We are running script from Jenkins server - path needs to be changed")
    #results_log = os.getcwd() + "/" + espn_results_file
    results_log = os.getcwd() + "/testing/" + espn_results_file
    run_type = "jenkins"
    print("Path for results file has been set, type set to jenkins")
else:
    print("We are running script from development VM")
    #results_log = test_folder_path + "/" + test_name + "/" + espn_results_file
    results_log = os.getcwd() + "/testing/" + espn_results_file
    print("Path for results file has been set, type set to manual")

print("Results log: ", results_log)
print("Connecting to Credence ...")

try:
    config = {
        'user': 'selenium',
        'password': 'Selenium#123#',
        'host': '192.168.239.1',
        'database': 'selenium',
    }
    cnx = mysql.connector.connect(**config)
except Exception as f:
    print(f)
    print("Was not ale to connect to MYSQL - will sleep and try again")
    time.sleep(10)

    config = {
        'user': 'selenium',
        'password': 'Selenium#123#',
        'host': '192.168.239.1',
        'database': 'selenium',
    }
    cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

current_timestamp = datetime.now(pytz.timezone('America/Los_Angeles'))

# 2024-06-10 13:21:28.767966-07:00
print("Current time: ", current_timestamp)
print("")

print("Opening file to post to Credence ...")

try:
    text_file = open(results_log, "r")
    lines = text_file.readlines()

    ESPN_Home_trx_time = 'NULL'

    for line in lines:
        trx_name, trx_status, trx_duration, browser_type = line.split(",")

        #RuckusOne_New_BOM_Iteration = trx_duration.strip('\n\t\r')

        if trx_name == 'ESPN_Home':
            ESPN_Home_trx_time = trx_duration[:5]
            ESPN_Home_trx_status = trx_status

        if trx_name == 'ESPN_Wrapper':
            ESPN_Wrapper_trx_status = trx_status
            if ESPN_Wrapper_trx_status == 'Fail' or ESPN_Wrapper_trx_status == 'Stop':
                ESPN_Wrapper_trx_time = 'NULL'
            else:
                ESPN_Wrapper_trx_time = trx_duration[:5]

        if trx_name == 'ESPN_Heartbeat':
            ESPN_Heartbeat_trx_status = trx_status
            if ESPN_Heartbeat_trx_status == 'Fail' or ESPN_Heartbeat_trx_status == 'Stop':
                ESPN_Heartbeat_trx_time = 'NULL'
            else:
                ESPN_Heartbeat_trx_time = trx_duration[:5]

    print("Inserting results into database ...")

    cursor.execute(
        """INSERT INTO espn_heartbeat(RunTimeStamp, RunType, Home, Browser)
                      values (%s, %s, %s, %s)""",
        (current_timestamp, run_type, ESPN_Home_trx_time, browser_type))

    cnx.commit()
    cursor.close()

    cnx.close()
    text_file.close()

except Exception as e:
    print("We have hit an exception")
    errors.append(str(e))

if errors:
    print("Will tell Jenkins about the errors...")
    print(f"ERROR: {errors}")
    sys.exit(1)  # tells Jenkins: FAILED
else:
    print("Will tell Jenkins everything is fine")
    print("All good!")
    sys.exit(0)  # tells Jenkins: SUCCESS
