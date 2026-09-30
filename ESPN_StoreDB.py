import os
import sys
import csv
import unicodedata
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

# ============================================================
# Allowed Browser Values
#
# Only these four values may ever be stored in the Browser
# column. Matching is case-insensitive and ignores hidden
# characters; the canonical spelling below is what gets stored.
# ============================================================

ALLOWED_BROWSERS = ("Chrome", "Edge", "Firefox", "Safari")

# Lower-case lookup of accepted spellings -> canonical value.
BROWSER_LOOKUP = {name.lower(): name for name in ALLOWED_BROWSERS}

# Common alternate names that map onto the four allowed values.
BROWSER_LOOKUP.update({
    "google chrome": "Chrome",
    "microsoft edge": "Edge",
    "msedge": "Edge",
    "mozilla firefox": "Firefox",
})


def clean_text(value):
    """
    Remove control/format characters (CR, LF, tab, zero-width
    space, BOM), convert non-breaking spaces to regular spaces,
    and trim the result.
    """
    value = "".join(
        ch for ch in value
        if unicodedata.category(ch) not in ("Cc", "Cf")
    )
    return value.replace("\xa0", " ").strip()


def normalize_browser(value):
    """
    Return the canonical browser name (Chrome, Edge, Firefox or
    Safari) for the given raw value, or None if the value is not
    one of the allowed browsers.
    """
    cleaned = clean_text(value)
    return BROWSER_LOOKUP.get(cleaned.lower())


# ============================================================
# Load MySQL Environment
# ============================================================

def load_mysql_environment():
    """
    Load MySQL configuration.

    Jenkins:
        Read the Jenkins Secret File specified by ENV_FILE
        directly using python-dotenv.

    Local execution:
        Read the local .env file.

    The Jenkins Secret File is intentionally NOT sourced by
    the shell because shell interpretation can alter special
    characters in the password.
    """

    env_file = os.getenv("ENV_FILE")

    if env_file:

        print("Using Jenkins Secret File specified by ENV_FILE")

        if not os.path.isfile(env_file):
            print(
                f"ERROR: ENV_FILE does not exist: {env_file}"
            )
            sys.exit(1)

        # Read the Secret File directly.
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
    return (
        mysql_url,
        mysql_username,
        mysql_password
    )

# ============================================================
# Load MySQL Configuration
# ============================================================

mysql_url, mysql_username, mysql_password = load_mysql_environment()

print("")
print("MySQL configuration:")
print(f"  MYSQL_URL      : {mysql_url}")
print(f"  MYSQL_USERNAME : {mysql_username}")

if mysql_password:
    print(
        f"  MYSQL_PASSWORD : SET "
        f"({len(mysql_password)} characters)"
    )
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

print("")
print(f"Results file: {espn_results_file}")
print(f"Run type: {run_type}")

# ============================================================
# Verify Results File
# ============================================================

if not os.path.exists(espn_results_file):
    print(
        f"ERROR: Results file was not found: "
        f"{espn_results_file}"
    )
    sys.exit(1)

# ============================================================
# Read Test Results
#
# utf-8-sig transparently removes a BOM if the file has one.
# ============================================================

try:
    with open(
        espn_results_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        results = list(
            csv.reader(file)
        )
except Exception as e:
    print(
        f"ERROR: Unable to read results file: {e}"
    )
    sys.exit(1)

# ============================================================
# Parse Results
#
# File format produced by ESPN_WriteResult.py:
#
# TransactionName,Status,Duration,Browser
#
# Example:
#
# ESPN_Home,Pass,15.4316,Chrome
# ESPN_NBA,Pass,5.1414,Chrome
# ESPN_Fantasy,Pass,7.3384,Chrome
#
# ============================================================

home_duration = None
nba_duration = None
fantasy_duration = None
browser = None
invalid_browser_values = []

print("")
print("Reading Selenium results file...")
print("")

for row in results:
    # Ignore empty rows
    if not row:
        continue
    # Display the raw row for troubleshooting
    print(f"Result row: {row}")
    # We expect:
    #
    # [0] Transaction Name
    # [1] Status
    # [2] Duration
    # [3] Browser

    if len(row) < 4:
        print(
            f"WARNING: Ignoring malformed result row: {row}"
        )
        continue

    transaction_name = clean_text(row[0])
    transaction_status = clean_text(row[1])
    transaction_time = clean_text(row[2])
    raw_browser = row[3]

    # --------------------------------------------------------
    # Browser
    #
    # Only Chrome, Edge, Firefox and Safari are accepted.
    # Anything else is recorded and causes the run to fail
    # validation below (nothing is inserted).
    # --------------------------------------------------------
    if clean_text(raw_browser):
        normalized_browser = normalize_browser(raw_browser)

        if normalized_browser is None:
            invalid_browser_values.append(raw_browser)
        else:
            browser = normalized_browser
    # --------------------------------------------------------
    # Home
    # --------------------------------------------------------
    if transaction_name == "ESPN_Home":
        try:
            home_duration = float(
                transaction_time
            )
        except ValueError:
            print(
                "ERROR: Invalid Home transaction duration: "
                f"{transaction_time}"
            )
    # --------------------------------------------------------
    # NBA
    # --------------------------------------------------------
    elif transaction_name == "ESPN_NBA":
        try:
            nba_duration = float(
                transaction_time
            )
        except ValueError:
            print(
                "ERROR: Invalid NBA transaction duration: "
                f"{transaction_time}"
            )
    # --------------------------------------------------------
    # Fantasy
    # --------------------------------------------------------
    elif transaction_name == "ESPN_Fantasy":
        try:
            fantasy_duration = float(
                transaction_time
            )
        except ValueError:
            print(
                "ERROR: Invalid Fantasy transaction duration: "
                f"{transaction_time}"
            )
# ============================================================
# Display Parsed Results
# ============================================================

print("")
print("============================================================")
print(" Parsed Selenium Results")
print("============================================================")

print(f"Browser : {browser}")
print(f"Home    : {home_duration}")
print(f"NBA     : {nba_duration}")
print(f"Fantasy : {fantasy_duration}")

print("============================================================")

# ============================================================
# Validate Browser
#
# Reject the run if any unrecognized browser value was found.
# repr() is used so hidden characters are visible in the log.
# ============================================================

if invalid_browser_values:
    print("")
    print(
        "ERROR: Unrecognized Browser value(s) in results file: "
        + ", ".join(repr(v) for v in invalid_browser_values)
    )
    print(
        "Allowed values: " + ", ".join(ALLOWED_BROWSERS)
    )
    print("")
    print(
        "The results will NOT be inserted into MySQL."
    )
    sys.exit(1)

# ============================================================
# Validate Parsed Results
# ============================================================
#
# Do NOT insert NULL values into MySQL if the results file
# could not be parsed correctly.
# ============================================================

missing_results = []

if browser is None:
    missing_results.append("Browser")

if home_duration is None:
    missing_results.append("Home")

if nba_duration is None:
    missing_results.append("NBA")

if fantasy_duration is None:
    missing_results.append("Fantasy")

if missing_results:
    print("")
    print(
        "ERROR: Required Selenium result value(s) "
        "could not be parsed:"
    )
    for value in missing_results:
        print(f"  - {value}")
    print("")
    print(
        "The results will NOT be inserted into MySQL."
    )
    sys.exit(1)

# Final safety net: browser must be exactly one of the four values.
if browser not in ALLOWED_BROWSERS:
    print(
        f"ERROR: Browser value {browser!r} is not allowed. "
        "The results will NOT be inserted into MySQL."
    )
    sys.exit(1)

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
        f"MySQL connection failed: {err}"
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

    print("")
    print("Values being inserted:")
    print(f"  RunTimeStamp : {run_timestamp}")
    print(f"  RunType      : {run_type}")
    print(f"  Home         : {home_duration}")
    print(f"  NBA          : {nba_duration}")
    print(f"  Fantasy      : {fantasy_duration}")
    print(f"  Browser      : {browser}")
    print("")

    home_duration = round(float(home_duration), 2)
    nba_duration = round(float(nba_duration), 2)
    fantasy_duration = round(float(fantasy_duration), 2)

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
        f"ERROR: Failed to insert Selenium results: {err}"
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
