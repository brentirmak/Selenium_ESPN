#from selenium import webdriver

#from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta

import sys
import os
import time
import pytz
import argparse

import ESPN_Home
import ESPN_NBA
import ESPN_Fantasy
import ESPN_SetBrowser
import ESPN_SetupLogSnapshot
import ESPN_Parameters
import ESPN_WriteResult

debug_file_prefix = ESPN_Parameters.espn_test_parameters['DEBUG_FILE_PREFIX']
test_folder_path = ESPN_Parameters.espn_test_parameters['TEST_FOLDER_PATH']
test_name = ESPN_Parameters.espn_test_parameters['TEST_NAME']
run_type = "manual"

print("*****************************************")
print("Current working directory (Jenkins): ", os.getcwd())
print("*****************************************")
print("Test Folder Path (per script): ", test_folder_path + "/" + test_name)
print("*****************************************")

# File to store overall Heartbeat test information locally - also used for DB storing purposes
if "var/lib/jenkins/workspace" in os.getcwd():
    print("We are running script from Jenkins server - path needs to be changed")
    results_log_path = os.getcwd() + "/" + test_name + ".txt"
    run_type = "jenkins"
    print("Path for results file has been set, run type set to jenkins")
elif "/Users/seiwa/" in os.getcwd():
    print("We are running script from iOS - path needs to be changed")
    results_log_path = "/Users/seiwa/SeleniumProjects/Selenium_ESPN" + "/" + test_name + ".txt"
    print("Path for results file has been set, run type set to manual")
else:
    print("We are running script from development VM")
    results_log_path = test_folder_path + "/" + test_name + "/" + test_name + ".txt"
    print("Path for results file has been set, run type set to manual")

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--browser", default="Chrome")
args = parser.parse_args()

with open(results_log_path, 'w') as results_log:

    debug_log, error_snapshot_path = ESPN_SetupLogSnapshot.init()

    with open(debug_log, 'w') as debug_log:

        browser_type = args.browser
        print("Browser Type: ", browser_type)
        debug_log.write("Browser Type: ")
        debug_log.write(str(browser_type))
        debug_log.write("\n")

        debug_log.write("Setting up the driver for the browser\n")
        print("Setting up the driver for the browser")
        driver = ESPN_SetBrowser.init(browser_type, debug_log)
        debug_log.write("Driver for the browser has been set.\n")
        print("Driver for the browser has been set.")

        try:
            debug_log.write("*************** START: Wrapper Transaction ***************\n")
            print ("*************** START: Wrapper Transaction ***************")
            wrapper_transaction_start = time.time()

            if wrapper_transaction_start is None:
                debug_log.write("Problem occurred starting the Wrapper transaction - will attempt again\n")
                print ("Problem occurred starting the Wrapper transaction - will attempt again")
                wrapper_transaction_start = time.time()

            ESPN_Home.init(driver, browser_type, error_snapshot_path, results_log, debug_log)

            ESPN_NBA.init(driver, browser_type, error_snapshot_path, results_log, debug_log)

            ESPN_Fantasy.init(driver, browser_type, error_snapshot_path, results_log, debug_log)

            wrapper_transaction_end = time.time()

            if wrapper_transaction_end is None:
                debug_log.write("Problem occurred ending the Wrapper transaction - will attempt again\n")
                print ("Problem occurred ending the Wrapper transaction - will attempt again")
                wrapper_transaction_end = time.time()

            debug_log.write("*************** END: Wrapper Transaction ***************\n")
            print ("*************** END: Wrapper Transaction ***************")

            wrapper_transaction = wrapper_transaction_end - wrapper_transaction_start
            heartbeat_transaction = wrapper_transaction

            # Write To File for DB
            ESPN_WriteResult.init(results_log, "ESPN_Wrapper", "Pass", str(wrapper_transaction), browser_type)
            ESPN_WriteResult.init(results_log, "ESPN_Heartbeat", "Pass", str(heartbeat_transaction), browser_type)

        finally:
            driver.quit()
            debug_log.write("Browser closed.\n")
            print("Browser closed.\n")

            try:
                sys.exit()
            except SystemExit:
                debug_log.write("SystemExit Exception terminated the program!\n")
                print ("SystemExit Exception terminated the program!\n")
                quit()
