from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import sys

import ESPN_WriteResult

def init(driver, browser_type, error_snapshot_path, results_log, debug_log):
    try:
        debug_log.write("\n*************** START: NBA Transaction ***************\n")
        print("\n*************** START: NBA Transaction ***************")

        driver.set_page_load_timeout(90)

        nba_transaction_start = time.time()

        print("Checking for NBA menu item")
        debug_log.write("Checking for NBA menu item\n")

        driver.execute_script("window.scrollTo(0, 0);")


        driver.get("https://www.espn.com/nba/")

        # The following doesn't work in headless mode as the menu isn't available
        '''
        nba_menu_item = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "(//span[@class='link-text'][contains(.,'NBA')])[1]")))
        nba_menu_item.click()
        '''

        print("Clicked on NBA menu item")
        debug_log.write("Clicked on NBA menu item\n")

        print("Checking for the NBA logo")
        debug_log.write("Checking for the NBA logo\n")

        nba_logo = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//img[@title='NBA']")))

        print("NBA logo found")
        debug_log.write("NBA logo found\n")

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

        nba_transaction_end = time.time()

        debug_log.write("*************** END: NBA Transaction ***************\n")
        print("*************** END: NBA Transaction ***************")

        nba_transaction = nba_transaction_end - nba_transaction_start

        debug_log.write("\nNBA Transaction Duration: ")
        debug_log.write(str(nba_transaction))
        debug_log.write("\n")

        print("\nNBA Transaction Duration: ", str(nba_transaction))

        ESPN_WriteResult.init(results_log, "ESPN_NBA", "Pass", str(nba_transaction), browser_type)
    except Exception as err:

        print("Exception: ", err)
        debug_log.write("\nException: ")
        debug_log.write(str(err))

        print("Capturing screenshot")
        debug_log.write("Capturing screenshot\n")

        # Example: Take a screenshot
        home_error_snapshot = error_snapshot_path + "_NBA.png"
        driver.save_screenshot(home_error_snapshot)
        debug_log.write("Captured Error Screenshot: ")
        debug_log.write(home_error_snapshot)
        debug_log.write("\n")
        print("\nCaptured Error Screenshot: ", home_error_snapshot)

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
    ESPN_WriteResult.init(results_log, "ESPN_NBA", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Wrapper", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Heartbeat", "Fail", "NULL", browser_type)
