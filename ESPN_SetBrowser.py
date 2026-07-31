from selenium import webdriver

def init(browser_type, debug_log):
    if "Chrome" in browser_type:
        print("Driver settings for Chrome should be set.")
        debug_log.write("Driver settings for Chrome should be set.\n")

        from selenium.webdriver.chrome.options import Options

        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver settings for Chrome have been set.")
        debug_log.write("Driver settings for Chrome have been set.\n")

        return driver
    elif "Firefox" in browser_type:
        print("Driver settings for Firefox should be set.")
        debug_log.write("Driver settings for Firefox should be set.\n")

        from selenium.webdriver.firefox.options import Options

        # Configure FireFox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless=new")
        firefox_options.add_argument("--disable-blink-features=AutomationControlled")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0")

        # Initialize the driver
        driver = webdriver.Firefox(options=firefox_options)
        print("Driver settings for Firefox have been set.")
        debug_log.write("Driver settings for Firefox have been set.\n")

        return driver
    elif "Edge" in browser_type:
        print("Driver settings for Edge should be set.")
        debug_log.write("Driver settings for Edge should be set.\n")

        from selenium.webdriver.edge.options import Options

        # Configure Edge options
        edge_options = Options()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        edge_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")

        # Initialize the driver
        driver = webdriver.Edge(options=edge_options)
        print("Driver settings for Edge have been set.")
        debug_log.write("Driver settings for Edge have been set.\n")

        return driver
<<<<<<< HEAD
    elif "Safari" in browser_type:
        print("Driver settings for Edge should be set.")
        debug_log.write("Driver settings for Safari should be set.\n")
    
        from selenium.webdriver.safari.options import Options
    
        # Configure Safari options
        safari_options = Options()
        safari_options.add_argument("--headless=new")
        safari_options.add_argument("--disable-blink-features=AutomationControlled")
        safari_options.add_argument("--no-sandbox")
        safari_options.add_argument("--disable-dev-shm-usage")
        safari_options.add_argument("--disable-gpu")
        safari_options.add_argument("--window-size=1920,1080")
        safari_options.add_argument(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15")
    
        # Initialize the driver
        driver = webdriver.Safari(options=safari_options)
        print("Driver settings for Safari have been set.")
        debug_log.write("Driver settings for Safari have been set.\n")
    
        return driver
=======
>>>>>>> origin/master
    else:
        print("Default driver settings should be set.")
        debug_log.write("Default driver settings should be set.\n")

        from selenium.webdriver.chrome.options import Options

        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        print("Default driver settings have been set.")
        debug_log.write("Default driver settings have been set.\n")

        return driver