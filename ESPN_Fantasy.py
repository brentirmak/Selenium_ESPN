from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import sys

import ESPN_WriteResult

def init(driver, browser_type, error_snapshot_path, results_log, debug_log):
    try:
        debug_log.write("\n*************** START: Fantasy Transaction ***************\n")
        print("\n*************** START: Fantasy Transaction ***************")

        driver.set_page_load_timeout(90)

        fantasy_transaction_start = time.time()

        print("Checking for Fantasy menu item")
        debug_log.write("Checking for Fantasy menu item\n")

        driver.execute_script("window.scrollTo(0, 0);")

        driver.get("https://www.espn.com/fantasy/")

        fantasy_header = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(.,'Fantasy')]")))

        print("Fantasy header found")
        debug_log.write("Fantasy header found\n")

        print("Scrolling to the bottom of the page")
        debug_log.write("Scrolling to the bottom of the page\n")

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # wait for content to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # reached the bottom
            last_height = new_height

        print("Checking the presence of the Work for ESPN text")
        debug_log.write("Checking the presence of the Work for ESPN text\n")

        work_for_espn_text = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "(//a[contains(.,'Work for ESPN')])[2]")))

        print("Work for ESPN text found")
        debug_log.write("Work for ESPN text found\n")

        fantasy_transaction_end = time.time()

        debug_log.write("*************** END: Fantasy Transaction ***************\n")
        print("*************** END: Fantasy Transaction ***************")

        fantasy_transaction = fantasy_transaction_end - fantasy_transaction_start

        debug_log.write("\nFantasy Transaction Duration: ")
        debug_log.write(str(fantasy_transaction))
        debug_log.write("\n")

        print("\nFantasy Transaction Duration: ", str(fantasy_transaction))

        ESPN_WriteResult.init(results_log, "ESPN_Fantasy", "Pass", str(fantasy_transaction), browser_type)
    except Exception as err:

        print("Exception: ", err)
        debug_log.write("\nException: ")
        debug_log.write(str(err))

        print("Capturing screenshot")
        debug_log.write("Capturing screenshot\n")

        # Example: Take a screenshot
        fantasy_error_snapshot = error_snapshot_path + "_Fantasy.png"
        driver.save_screenshot(fantasy_error_snapshot)
        debug_log.write("Captured Error Screenshot: ")
        debug_log.write(fantasy_error_snapshot)
        debug_log.write("\n")
        print("\nCaptured Error Screenshot: ", fantasy_error_snapshot)

        write_failure_to_log(results_log, browser_type)

        driver.close()
        time.sleep(1)
        driver.quit()

        try:
            sys.exit(1)
        except SystemExit:
            print("SystemExit Exception terminated the program!")
            quit()

def write_failure_to_log(results_log, browser_type):
    ESPN_WriteResult.init(results_log, "ESPN_Fantasy", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Wrapper", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Heartbeat", "Fail", "NULL", browser_type)
