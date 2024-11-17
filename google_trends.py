from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from enum import Enum
import json
import time

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_data_dir = "/Users/patrykszmajduch/Library/Application Support/Google/Chrome"
# time range
class DateRange(Enum):
    ONE_MONTH = "today%201-m"
    FOUR_HOURS = "now%204-H"
    ONE_HOUR = "now%201-H"
    ONE_DAY = "now%201-d"
    ONE_WEEK = "now%207-d"
def get_driver():
    # update the path to the location of your Chrome binary
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--headless=new")
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})  # Equivalent to desired_capabilities
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches",
                                    ["enable-automation", "enable-logging"])  # Remove automation warning
    driver = webdriver.Chrome(options=options)
    return driver
def get_data_from_gg_trends(keywords:[str], date_range = DateRange.ONE_MONTH, geo = "" ):
    driver = get_driver()
    result = dict[str,str]
    for key in keywords:
        get_raw_trends_data(driver, date_range.value, geo, key)
        logs = driver.get_log('performance')
        result = [key,extract_data_from_logs(driver,key, logs)]
    driver.quit()
    return result
def get_raw_trends_data(driver: webdriver.Chrome, date_range: str, geo: str, query: str) -> str:
    # &geo={geo} //not needed for now
    print("start get_raw_trends_data")
    url = f"https://trends.google.com/trends/explore?date=today%201-m&q={query}"
    print(f"Getting data from {url}")
    # After creating the driver instance
    driver.get(url)
    # workaround to get the page source after initial 429 error
    driver.get(url)

    driver.maximize_window()
    # Wait for the page to load
    time.sleep(1)
    driver.page_source

# Function to retrieve response body by request ID
def get_response_body(driver,log_entry):
    try:
        print("retrieving body")
        # Access the request ID
        request_id = log_entry["message"]["params"]["requestId"]

        # Send a CDP command to get the response body for the specific request ID
        response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        return response_body
    except Exception as e:
        print(f"Could not retrieve response body: {e}")
        return None

def extract_data_from_logs(driver, key, logs) ->  str:
    for entry in logs:
        log = json.loads(entry["message"])  # Parse the JSON message
        # Check if it is a response
        # if log["message"]["method"] == "Network.requestWillBeSent":
        #     try:
        #         # Extract the response URL
        #         url = log["message"]["params"]["request"]["url"]
        #
        #         # Check if "multi" is in the URL
        #         if "multi" in url:
        #             print(f"Filtered request URL: {url}")
        #     except KeyError:
        #         continue
        if log["message"]["method"] == "Network.responseReceived":
            try:
                # Extract the response URL
                url = log["message"]["params"]["response"]["url"]
                if "multi" in url:
                    print(f'multi url response for :{url}')
                    body = get_response_body(driver, log)
                    if "Error" in body['body']:
                        continue
                    else:
                        return body
            except KeyError:
                # Skip log entries that don't have a URL or response details
                continue