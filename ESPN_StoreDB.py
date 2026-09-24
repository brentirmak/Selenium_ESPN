import os
import sys
import mysql.connector
from datetime import datetime
import pytz
import ESPN_Parameters

from dotenv import load_dotenv, dotenv_values


# ============================================================
# Configuration
# ============================================================

espn_results_file = ESPN_Parameters.espn_test_parameters['RESULTS_FILE']
test_folder_path = ESPN_Parameters.espn_test_parameters['TEST_FOLDER_PATH']
test_name = ESPN_Parameters.espn_test_parameters['TEST_NAME']

run_type = "manual"

errors = []


# ============================================================
# Load MySQL Environment
# ============================================================

def load_mysql_environment():
    """
    Load MySQL configuration.

    Jenkins:
        Read the Jenkins Secret File specified by ENV_FILE
        using python-dotenv.

    Local execution:
        Read the local .env file.
    """

    env_file = os.getenv("ENV_FILE")

    if env_file:

        print("Using Jenkins Secret File specified by ENV_FILE")

        if not os.path.isfile(env_file):
            print(f"ERROR: ENV_FILE does not exist: {env_file}")
            sys.exit(1)

        # Read the Secret File directly.
        # Do NOT use shell sourcing.
        env = dotenv_values(env_file)

        mysql_url = env.get("MYSQL_URL")
        mysql_username = env.get("MYSQL_USERNAME")
        mysql_password = env.get("MYSQL_PASSWORD")

    else:

        print("Using local .env file")

        load_dotenv()

        mysql_url = os.getenv("MYSQL_URL")
        mysql_username = os.getenv("MYSQL_USERNAME")
        mysql_password = os.getenv("MYSQL_PASSWORD")

    return mysql_url, mysql_username, mysql_password


# ============================================================
# Load MySQL Configuration
# ============================================================

mysql_url, mysql_username, mysql_password = load_mysql_environment()


print("")
print("MySQL configuration:")
print(f"  MYSQL_URL      : {mysql_url}")
print(f"  MYSQL_USERNAME : {mysql_username}")

if mysql_password:
    print(f"  MYSQL_PASSWORD : SET ({len(mysql_password)} characters)")
else:
    print("  MYSQL_PASSWORD : NOT SET")


# ============================================================
# Validate MySQL Configuration
# ============================================================

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
# Determine Run Type / Paths
# ============================================================

current_path = os.getcwd()


if "var/lib/jenkins/workspace" in current_path:

    print(
        "We are running script from Jenkins server - "
        "path needs to be changed"
    )

    test_folder_path = current_path
    run_type = "jenkins"

elif "/Users/Shared/Jenkins/workspace" in current_path:

    print(
        "We are running script from Mac Jenkins server - "
        "path needs to be changed"
    )

    test_folder_path = current_path
    run_type = "jenkins"

elif "/Users/seiwa/" in current_path:

    run_type = "manual"

else:

    run_type = "manual"


# ============================================================
# Results File
# ============================================================

if run_type == "jenkins":

    espn_results_file = os.path.join(
        current_path,
        "Selenium_ESPN.txt"
    )

else:

    espn_results_file = os.path.join(
        test_folder_path,
        "Selenium_ESPN.txt"
    )


print(f"Results file: {espn_results_file}")
print(f"Run type: {run_type}")


# ============================================================
# Read Test Results
# ============================================================

if not os.path.exists(espn_results_file):

    print(
        f"ERROR: Results file was not found: "
        f"{espn_results_file}"
    )

    sys.exit(1)


try:

    with open(
        espn_results_file,
        "r",
        encoding="utf-8"
    ) as file:

        results = file.readlines()

except Exception as e:

    print(f"ERROR: Unable to read results file: {e}")

    sys.exit(1)


# ============================================================
# Parse Results
# ============================================================

home_duration = None
nba_duration = None
fantasy_duration = None
browser = None


for line in results:

    line = line.strip()

    # --------------------------------------------------------
    # Browser
    # --------------------------------------------------------

    if line.startswith("Browser Type:"):

        browser = line.split(":", 1)[1].strip()

    # --------------------------------------------------------
    # Home
    # --------------------------------------------------------

    elif line.startswith("Home Transaction Duration:"):

        try:

            home_duration = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass

    # --------------------------------------------------------
    # NBA
    # --------------------------------------------------------

    elif line.startswith("NBA Transaction Duration:"):

        try:

            nba_duration = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass

    # --------------------------------------------------------
    # Fantasy
    # --------------------------------------------------------

    elif line.startswith("Fantasy Transaction Duration:"):

        try:

            fantasy_duration = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


# ============================================================
# Display Parsed Results
# ============================================================

print("")
print("Parsed Selenium results:")
print(f"  Browser : {browser}")
print(f"  Home    : {home_duration}")
print(f"  NBA     : {nba_duration}")
print(f"  Fantasy : {fantasy_duration}")


# ============================================================
# MySQL Configuration
# ============================================================

config = {
    "user": mysql_username,
    "password": mysql_password,
    "host": mysql_url,
    "database": "selenium",
}


# ============================================================
# Connect To MySQL
# ============================================================

cnx = None
cursor = None


try:

    print("")
    print("Connecting to MySQL...")
    print(f"Host: {mysql_url}")
    print(f"User: {mysql_username}")

    cnx = mysql.connector.connect(
        **config
    )

    print("MySQL connection successful.")

    cursor = cnx.cursor()


except mysql.connector.Error as err:

    print(
        f"MySQL connection failed: "
        f"{err}"
    )

    sys.exit(1)


# ============================================================
# Timestamp
# ============================================================

try:

    pacific = pytz.timezone(
        "America/Los_Angeles"
    )

    run_timestamp = datetime.now(
        pacific
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

except Exception:

    run_timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ============================================================
# Insert Results
# ============================================================

insert_query = """
    INSERT INTO selenium_espn
    (
        RunTimeStamp,
        RunType,
        Home,
        NBA,
        Fantasy,
        Browser
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
"""


try:

    print("")
    print("Storing Selenium results in MySQL...")

    cursor.execute(
        insert_query,
        (
            run_timestamp,
            run_type,
            home_duration,
            nba_duration,
            fantasy_duration,
            browser,
        )
    )

    cnx.commit()

    print("")
    print("============================================================")
    print(" MySQL Insert Successful")
    print("============================================================")

    print(f"RunTimeStamp : {run_timestamp}")
    print(f"RunType      : {run_type}")
    print(f"Browser      : {browser}")
    print(f"Home         : {home_duration}")
    print(f"NBA          : {nba_duration}")
    print(f"Fantasy      : {fantasy_duration}")

    print("============================================================")


except mysql.connector.Error as err:

    print(
        f"ERROR: Failed to insert Selenium results: "
        f"{err}"
    )

    try:

        cnx.rollback()

    except Exception:

        pass

    sys.exit(1)


finally:

    if cursor is not None:

        try:
            cursor.close()
        except Exception:
            pass

    if cnx is not None:

        try:
            cnx.close()
        except Exception:
            pass


print("")
print("ESPN results successfully stored in MySQL.")