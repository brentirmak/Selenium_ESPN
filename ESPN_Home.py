from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import sys

import ESPN_Parameters
import ESPN_WriteResult
import ESPN_Alert

test_url = ESPN_Parameters.espn_test_parameters['TEST_URL']

#Alert Information
error_name = "ESPN Home"
error_detail = "ESPN Home transaction failed - look at the screenshot for the failure condition"

def init(driver, browser_type, error_snapshot_path, results_log, debug_log):

    try:
        debug_log.write("\n*************** START: Home Transaction ***************\n")
        print ("\n*************** START: Home Transaction ***************")

        driver.set_page_load_timeout(90)

        home_transaction_start = time.time()
        # Navigate to ESPN
        print("Navigate to ", str(test_url))
        debug_log.write("Navigate to http://www.espn.com/")
        driver.get(test_url)

        # Wait for the page to load (wait for body element)
        print("Wait for the page to load (wait for body element)")
        debug_log.write("Wait for the page to load (wait for body element)\n")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Print page title
        print(f"Page Title: {driver.title}")
        debug_log.write("Page Title: ")
        debug_log.write(driver.title)
        debug_log.write("\n")

        print("Checking for top headlines header")
        debug_log.write("Checking for top headlines header\n")

        top_headlines_header = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(.,'Top Headlines')]")))
        print(top_headlines_header.text)
        print("Top Headlines header found")
        debug_log.write("Top Headlines header found\n")

        print("---------------------------")
        #print("Id: ", top_headlines_header.get_attribute("id"))
        #print("Name: ", top_headlines_header.get_attribute("name"))
        #print("Type: ", top_headlines_header.get_attribute("type"))
        #print("Value: ",top_headlines_header.get_attribute("value"))
        #print("Class: ", top_headlines_header.get_attribute("class"))
        #print("Href: ", top_headlines_header.get_attribute("href"))
        #print("Src: ", top_headlines_header.get_attribute("src"))
        #print("Disabled: ", top_headlines_header.get_attribute("disabled"))
        #print("Data-id: ", top_headlines_header.get_attribute("data-id"))
        #print("innerHTML: ", top_headlines_header.get_attribute("innerHTML"))
        #print("outerHTML: ", top_headlines_header.get_attribute("outerHTML"))
        print("textContent: ", top_headlines_header.get_attribute("textContent"))
        print("---------------------------")

        print("Checking for ESPN logo")
        debug_log.write("Checking for ESPN logo\n")

        espn_logo = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(.,'ESPN')]")))

        print("---------------------------")
        #print("Id: ", espn_logo.get_attribute("id"))
        #print("Name: ", espn_logo.get_attribute("name"))
        #print("Type: ", espn_logo.get_attribute("type"))
        #print("Value: ",espn_logo.get_attribute("value"))
        #print("Class: ", espn_logo.get_attribute("class"))
        #print("Href: ", espn_logo.get_attribute("href"))
        #print("Src: ", espn_logo.get_attribute("src"))
        #print("Disabled: ", espn_logo.get_attribute("disabled"))
        #print("Data-id: ", espn_logo.get_attribute("data-id"))
        #print("innerHTML: ", espn_logo.get_attribute("innerHTML"))
        #print("outerHTML: ", espn_logo.get_attribute("outerHTML"))
        print("textContent: ", espn_logo.get_attribute("textContent"))
        print("---------------------------")


        print(espn_logo.text)
        print("ESPN logo found")
        debug_log.write("ESPN logo found\n")

        top_events_button = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(.,'Top Events')]")))

        print("---------------------------")
        #print("Id: ", top_events_button.get_attribute("id"))
        #print("Name: ", top_events_button.get_attribute("name"))
        #print("Type: ", top_events_button.get_attribute("type"))
        #print("Value: ",top_events_button.get_attribute("value"))
        #print("Class: ", top_events_button.get_attribute("class"))
        #print("Href: ", top_events_button.get_attribute("href"))
        #print("Src: ", top_events_button.get_attribute("src"))
        #print("Disabled: ", top_events_button.get_attribute("disabled"))
        #print("Data-id: ", top_events_button.get_attribute("data-id"))
        #print("innerHTML: ", top_events_button.get_attribute("innerHTML"))
        #print("outerHTML: ", top_events_button.get_attribute("outerHTML"))
        print("textContent: ", top_events_button.get_attribute("textContent"))
        print("---------------------------")

        time.sleep(5)

        print("Scrolling to the bottom of the page")
        debug_log.write("Scrolling to the bottom of the page\n")

        # Method 1
        ###driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Method 2
        #body = driver.find_element(By.TAG_NAME, "body")
        #body.send_keys(Keys.PAGE_DOWN)  # one page down
        #body.send_keys(Keys.END)  # jump to bottom

        # Method 3
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # wait for content to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # reached the bottom
            last_height = new_height

        terms_of_use_link = WebDriverWait(driver, 45). \
            until(EC.presence_of_element_located(
            (By.XPATH, "//*/div/footer/div[2]/div/div[2]/ul/li[1]/a")))

        # //a[normalize-space(.)='Contact Us']

        print("---------------------------")
        #print("Id: ", terms_of_use_link.get_attribute("id"))
        #print("Name: ", terms_of_use_link.get_attribute("name"))
        #print("Type: ", terms_of_use_link.get_attribute("type"))
        #print("Value: ",terms_of_use_link.get_attribute("value"))
        #print("Class: ", terms_of_use_link.get_attribute("class"))
        #print("Href: ", terms_of_use_link.get_attribute("href"))
        #print("Src: ", terms_of_use_link.get_attribute("src"))
        #print("Disabled: ", terms_of_use_link.get_attribute("disabled"))
        #print("Data-id: ", terms_of_use_link.get_attribute("data-id"))
        #print("innerHTML: ", terms_of_use_link.get_attribute("innerHTML"))
        #print("outerHTML: ", terms_of_use_link.get_attribute("outerHTML"))
        print("textContent: ", terms_of_use_link.get_attribute("textContent"))
        print("---------------------------")

        if terms_of_use_link.get_attribute("textContent") == "Terms of Use":
            print("Terms of Use link found - passing transaction")
            debug_log.write("Terms of Use link found - passing transaction\n")
            pass
        else:
            print("Terms of use link NOT found - failing transaction")

            print("Capturing screenshot")
            debug_log.write("Capturing screenshot\n")

            # Example: Take a screenshot
            home_error_snapshot = error_snapshot_path + "_Home.png"
            driver.save_screenshot(home_error_snapshot)
            debug_log.write("Captured Error Screenshot: ")
            debug_log.write(home_error_snapshot)
            debug_log.write("\n")
            print("\nCaptured Error Screenshot: ", home_error_snapshot)

            write_failure_to_log(results_log, browser_type)

            try:
                debug_log.write("Sending out alerts...\n")
                print("Sending out alerts...")

                ESPN_Alert.init(error_name, home_error_snapshot, error_detail)
            except:
                debug_log.write("Could not send out the alerts...\n")
                print("Could not send out the alerts...")

            driver.close()
            time.sleep(1)
            driver.quit()

            try:
                sys.exit(1)
            except SystemExit:
                print("SystemExit Exception terminated the program!")
                quit()

        home_transaction_end = time.time()

        debug_log.write("*************** END: Home Transaction ***************\n")
        print("*************** END: Home Transaction ***************")

        home_transaction = home_transaction_end - home_transaction_start

        debug_log.write("\nHome Transaction Duration: ")
        debug_log.write(str(home_transaction))
        debug_log.write("\n")

        print("\nHome Transaction Duration: ", str(home_transaction))

        ESPN_WriteResult.init(results_log, "ESPN_Home", "Pass", str(home_transaction), browser_type)
    except Exception as err:

        print ("Exception: ", err)
        debug_log.write("\nException: ")
        debug_log.write(str(err))

        print("Capturing screenshot")
        debug_log.write("Capturing screenshot\n")

        # Example: Take a screenshot
        home_error_snapshot = error_snapshot_path + "_Home.png"
        driver.save_screenshot(home_error_snapshot)
        debug_log.write("Captured Error Screenshot: ")
        debug_log.write(home_error_snapshot)
        debug_log.write("\n")
        print("\nCaptured Error Screenshot: ", home_error_snapshot)

        write_failure_to_log(results_log, browser_type)

        try:
            debug_log.write("Sending out alerts...\n")
            print("Sending out alerts...")

            ESPN_Alert.init(error_name, home_error_snapshot, error_detail)
        except:
            debug_log.write("Could not send out the alerts...\n")
            print("Could not send out the alerts...")

        driver.close()
        time.sleep(1)
        driver.quit()

        try:
            sys.exit(1)
        except SystemExit:
            print("SystemExit Exception terminated the program!")
            quit()

def write_failure_to_log(results_log, browser_type):
    ESPN_WriteResult.init(results_log, "ESPN_Home", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_NBA", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Fantasy", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Wrapper", "Fail", "NULL", browser_type)
    ESPN_WriteResult.init(results_log, "ESPN_Heartbeat", "Fail", "NULL", browser_type)
