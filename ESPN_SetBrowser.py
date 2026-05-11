from selenium import webdriver

def init(browser_type, debug_log):
    if "Chrome" in browser_type:
        print("Driver settings for Chrome should be set.")
        debug_log.write("Driver settings for Chrome should be set.\n")

        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options

        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver settings for Chrome have been set.")
        debug_log.write("Driver settings for Chrome have been set.\n")

        return driver
    elif "Firefox" in browser_type:
        print("Driver settings for Firefox should be set.")
        debug_log.write("Driver settings for Firefox should be set.\n")

        from selenium.webdriver.firefox.service import Service
        from selenium.webdriver.firefox.options import Options

        # Configure FireFox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Firefox(options=firefox_options)
        print("Driver settings for Firefox have been set.")
        debug_log.write("Driver settings for Firefox have been set.\n")

        return driver
    elif "Edge" in browser_type:
        print("Driver settings for Edge should be set.")
        debug_log.write("Driver settings for Edge should be set.\n")

        from selenium.webdriver.edge.service import Service
        from selenium.webdriver.edge.options import Options

        # Configure Edge options
        edge_options = Options()
        edge_options.add_argument("--headless")  # Run in headless mode (no browser window)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        #edge_options.add_argument(
        #    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Edge(options=edge_options)
        print("Driver settings for Edge have been set.")
        debug_log.write("Driver settings for Edge have been set.\n")

        return driver
    else:
        print("Default driver settings should be set.")
        debug_log.write("Default driver settings should be set.\n")
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        print("Default driver settings have been set.")
        debug_log.write("Default driver settings have been set.\n")

        return driver