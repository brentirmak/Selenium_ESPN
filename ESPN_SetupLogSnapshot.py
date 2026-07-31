import os
import time
import pytz
from datetime import datetime, timedelta

import ESPN_Parameters

debug_file_prefix = ESPN_Parameters.espn_test_parameters['DEBUG_FILE_PREFIX']
test_folder_path = ESPN_Parameters.espn_test_parameters['TEST_FOLDER_PATH']
test_name = ESPN_Parameters.espn_test_parameters['TEST_NAME']
run_type = "manual"

def init():
    datetime_in_us_pacific = datetime.now(pytz.timezone('America/Los_Angeles'))

    # Path for snapshot on errors and path for debug log files
    if "var/lib/jenkins/workspace" in os.getcwd():
        print("We are running script from Jenkins server - path needs to be changed")
        error_snapshot_path = os.getcwd() + "/" + test_name + "/Error_Snapshots/"
        debug_log_path = os.getcwd() + "/" + test_name + "/Debug/"
        run_type = "jenkins"
        print("Path for error snapshots and debug logs has been set, run type set to jenkins")
    elif "/Users/seiwa/" in os.getcwd():
        print("We are running script from iOS - path needs to be changed")
        error_snapshot_path = "/Users/seiwa/SeleniumProjects/Selenium_ESPN/Error_Snapshots/"
        debug_log_path = "/Users/seiwa/SeleniumProjects/Selenium_ESPN/Debug/"
        print("Path for error snapshots and debug logs has been set, run type set to manual")
    else:
        print("We are running script from development VM")
        error_snapshot_path = test_folder_path + "/" + test_name + "/Error_Snapshots/"
        debug_log_path = test_folder_path + "/" + test_name + "/Debug/"
        print("Path for error snapshots and debug logs has been set, run type set to manual")

    # Capture current date to set to label all log files with script runtime/timestamp information
    # file_timestamp = time.strftime("%H%M_%m%d%Y")
    file_timestamp = datetime_in_us_pacific.strftime("%H%M_%m%d%Y")
    print("File timestamp: ", str(file_timestamp))
    # debug_log.write("File timestamp: ")
    # debug_log.write(str(file_timestamp))
    # debug_log.write("\n")

    # Set folder name (using current day and month)
    # script_debug_folder = time.strftime("%m%d")
    script_debug_folder = datetime_in_us_pacific.strftime("%m%d")
    print("Script Debug Folder: ", str(script_debug_folder))
    # debug_log.write("Script Debug Folder: ")
    # debug_log.write(str(script_debug_folder))
    # debug_log.write("\n")

    # Set the path for error snapshots
    error_snapshot_path_dir = error_snapshot_path + script_debug_folder
    error_snapshot_path = error_snapshot_path_dir + "/"
    error_snapshot_path = error_snapshot_path + file_timestamp

    # Set the path for debug logs
    debug_log_path = debug_log_path + script_debug_folder
    debug_log_path = debug_log_path + "/"

    # Create snapshot folder if it doesn't exist already
    if not os.path.exists(error_snapshot_path_dir):
        # debug_log.write("Creating snapshot folder - it doesn't exist\n")
        print("Creating snapshot folder - it doesn't exist")
        os.makedirs(error_snapshot_path_dir)

    # Create debug log folder if it doesn't exist already
    if not os.path.exists(debug_log_path):
        # debug_log.write("Creating debug log folder - it doesn't exist\n")
        print("Creating debug log folder - it doesn't exist")
        os.makedirs(debug_log_path)

    # Set the path for debug files
    debug_log = debug_log_path + debug_file_prefix + file_timestamp + ".txt"
    print("Path for debug log has been set\n")

    return debug_log, error_snapshot_path