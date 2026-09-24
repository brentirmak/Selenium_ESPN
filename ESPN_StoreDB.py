import os
import sys
import mysql.connector
import pytz
from datetime import datetime

import ESPN_Parameters
from dotenv import load_dotenv


# ============================================================
# Configuration
# ============================================================

espn_results_file = ESPN_Parameters.espn_test_parameters['RESULTS_FILE']
test_folder_path = ESPN_Parameters.espn_test_parameters['TEST_FOLDER_PATH']
test_name = ESPN_Parameters.espn_test_parameters['TEST_NAME']

run_type = "manual"
errors = []

cnx = None
cursor = None


# ============================================================
# Load environment variables
# ============================================================
#
# Jenkins provides the variables from the Secret File bound to
# ENV_FILE.  In Jenkins, do NOT allow a local .env file to
# override those values.
#
# For local development, if ENV_FILE is not set, load .env.
# ============================================================

if os.getenv("ENV_FILE"):
    print("Using environment variables provided by Jenkins ENV_FILE")
else:
    print("ENV_FILE is not set - loading local .env file")
    load_dotenv()


# Retrieve MySQL configuration
mysql_url = os.getenv("MYSQL_URL")
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")


# ============================================================
# Validate MySQL configuration
# ============================================================

print("")
print("MySQL configuration:")
print(f"  MYSQL_URL      : {mysql_url}")
print(f"  MYSQL_USERNAME : {mysql_username}")
print(
    f"  MYSQL_PASSWORD : "
    f"{'********' if mysql_password else 'NOT SET'}"
)
print("")


missing_variables = []

if not mysql_url:
    missing_variables.append("MYSQL_URL")

if not mysql_username:
    missing_variables.append("MYSQL_USERNAME")

if not mysql_password:
    missing_variables.append("MYSQL_PASSWORD")

if missing_variables:
    print(
        "ERROR: Missing required MySQL environment variable(s): "
        + ", ".join(missing_variables)
    )
    sys.exit(1)


# ============================================================
# Determine results log location
# ============================================================

current_directory = os.getcwd()

if "var/lib/jenkins/workspace" in current_directory:
    print("Running from Jenkins")
    results_log = os.path.join(current_directory, espn_results_file)
    run_type = "jenkins"

elif "/Users/Shared/Jenkins/workspace" in current_directory:
    print("Running from Jenkins - MacOS")
    results_log = os.path.join(current_directory, espn_results_file)
    run_type = "jenkins"

elif "/Users/seiwa/" in current_directory:
    print("We are running script from iOS")
    results_log = os.path.join(
        "/Users/seiwa/SeleniumProjects/Selenium_ESPN",
        espn_results_file
    )

else:
    print("Running from dev VM")
    results_log = os.path.join(
        test_folder_path,
        test_name,
        espn_results_file
    )


print("Results log:", results_log)


# ============================================================
# Validate results file
# ============================================================

if not os.path.exists(results_log):
    print(f"ERROR: Results file not found: {results_log}")
    sys.exit(1)


# ============================================================
# Database connection
# ============================================================

def connect_to_db(config):
    try:
        return mysql.connector.connect(**config)

    except mysql.connector.Error as e:
        print(f"DB connection failed: {e}")
        return None

    except Exception as e:
        print(f"Unexpected DB connection error: {e}")
        return None


config = {
    "user": mysql_username,
    "password": mysql_password,
    "host": mysql_url,
    "database": "selenium",
}


print("Connecting to DB...")

cnx = connect_to_db(config)

if cnx is None:
    print("ERROR: Unable to connect to MySQL.")
    print(f"Host used: {mysql_url}")
    print(f"Username used: {mysql_username}")
    sys.exit(1)


cursor = cnx.cursor()


# ============================================================
# Main logic
# ============================================================

try:

    current_timestamp = datetime.now(
        pytz.timezone("America/Los_Angeles")
    )

    print("Current time:", current_timestamp)

    with open(results_log, "r") as text_file:
        lines = text_file.readlines()


    # Default values
    ESPN_Home_trx_time = "NULL"
    ESPN_NBA_trx_time = "NULL"
    ESPN_Fantasy_trx_time = "NULL"

    browser_type = "Unknown"


    # ========================================================
    # Parse results file
    # ========================================================

    for line in lines:

        line = line.strip()

        if not line:
            continue

        try:
            trx_name, trx_status, trx_duration, browser_type = (
                line.split(",")
            )

        except ValueError:
            print(f"WARNING: Unable to parse results line: {line}")
            continue


        if trx_name == "ESPN_Home":

            ESPN_Home_trx_time = trx_duration[:5]
            ESPN_Home_trx_status = trx_status


        elif trx_name == "ESPN_NBA":

            ESPN_NBA_trx_time = trx_duration[:5]
            ESPN_NBA_trx_status = trx_status


        elif trx_name == "ESPN_Fantasy":

            ESPN_Fantasy_trx_time = trx_duration[:5]
            ESPN_Fantasy_trx_status = trx_status


        elif trx_name == "ESPN_Wrapper":

            ESPN_Wrapper_trx_status = trx_status

            ESPN_Wrapper_trx_time = (
                "NULL"
                if ESPN_Wrapper_trx_status in ("Fail", "Stop")
                else trx_duration[:5]
            )


        elif trx_name == "ESPN_Heartbeat":

            ESPN_Heartbeat_trx_status = trx_status

            ESPN_Heartbeat_trx_time = (
                "NULL"
                if ESPN_Heartbeat_trx_status in ("Fail", "Stop")
                else trx_duration[:5]
            )


    # ========================================================
    # Insert results
    # ========================================================

    print("Inserting results into DB...")

    cursor.execute(
        """
        INSERT INTO selenium_espn
        (
            RunTimeStamp,
            RunType,
            Home,
            NBA,
            Fantasy,
            Browser
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            current_timestamp,
            run_type,
            ESPN_Home_trx_time,
            ESPN_NBA_trx_time,
            ESPN_Fantasy_trx_time,
            browser_type,
        ),
    )

    cnx.commit()

    print("Insert successful")


except Exception as e:

    print(f"ERROR: {e}")
    errors.append(str(e))


finally:

    if cursor is not None:
        cursor.close()

    if cnx is not None:
        cnx.close()


# ============================================================
# Final exit
# ============================================================

if errors:

    print(f"Job FAILED with errors: {errors}")
    sys.exit(1)

else:

    print("Job completed successfully")
    sys.exit(0)
```
