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

# --- Path setup ---
if "var/lib/jenkins/workspace" in os.getcwd():
    print("Running from Jenkins")
    results_log = os.getcwd() + "/testing/" + espn_results_file
    run_type = "jenkins"
else:
    print("Running from dev VM")
    results_log = os.getcwd() + "/testing/" + espn_results_file

print("Results log: ", results_log)

# Validate path exists before continuing
if not os.path.exists(results_log):
    print(f"ERROR: Results file not found: {results_log}")
    sys.exit(1)  # fail immediately — no point continuing

# --- DB connection ---
def connect_to_db(config):
    try:
        return mysql.connector.connect(**config)
    except Exception as e:
        print(f"DB connection failed: {e}")
        sys.exit(1)  # fail fast, no silent retry masking

config = {
    'user': 'selenium',
    'password': 'Selenium#123#',
    'host': '192.168.239.1',
    'database': 'selenium',
}

print("Connecting to DB...")
cnx = connect_to_db(config)
cursor = cnx.cursor()

# --- Main logic ---
try:
    current_timestamp = datetime.now(pytz.timezone('America/Los_Angeles'))
    print("Current time: ", current_timestamp)

    with open(results_log, "r") as text_file:
        lines = text_file.readlines()

    ESPN_Home_trx_time = 'NULL'
    for line in lines:
        trx_name, trx_status, trx_duration, browser_type = line.split(",")

        if trx_name == 'ESPN_Home':
            ESPN_Home_trx_time = trx_duration[:5]
            ESPN_Home_trx_status = trx_status
        if trx_name == 'ESPN_Wrapper':
            ESPN_Wrapper_trx_status = trx_status
            ESPN_Wrapper_trx_time = 'NULL' if ESPN_Wrapper_trx_status in ('Fail', 'Stop') else trx_duration[:5]
        if trx_name == 'ESPN_Heartbeat':
            ESPN_Heartbeat_trx_status = trx_status
            ESPN_Heartbeat_trx_time = 'NULL' if ESPN_Heartbeat_trx_status in ('Fail', 'Stop') else trx_duration[:5]

    print("Inserting results into DB...")
    cursor.execute(
        """INSERT INTO espn_heartbeat(RunTimeStamp, RunType, Home, Browser)
           VALUES (%s, %s, %s, %s)""",
        (current_timestamp, run_type, ESPN_Home_trx_time, browser_type)
    )
    cnx.commit()
    print("Insert successful")

except Exception as e:
    print(f"ERROR: {e}")
    errors.append(str(e))

finally:
    cursor.close()
    cnx.close()

# --- Final exit ---
if errors:
    print(f"Job FAILED with errors: {errors}")
    sys.exit(1)   # Jenkins sees FAILURE
else:
    print("Job completed successfully")
    sys.exit(0)   # Jenkins sees SUCCESS