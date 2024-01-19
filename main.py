import requests
from bs4 import BeautifulSoup
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pygetwindow as gw
import pyautogui
import math

# Adjust the number of proxy addresses to fetch
NUM_PROXIES_TO_FETCH = 5
# Adjust the URL to be opened in all browser windows
TARGET_URL = "http://httpbin.org/ip"


driver_instances_lock = threading.Lock()

def get_proxy_addresses():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        proxy_addresses = []
        
        table = soup.find('div', class_='table-responsive fpl-list')
        
        if table:
            rows = table.find('tbody').find_all('tr')
            
            for row in rows[:NUM_PROXIES_TO_FETCH]:
                cells = row.find_all('td')
                if len(cells) >= 1:
                    proxy_addresses.append(cells[0].text)
        
        return proxy_addresses
    else:
        print(f"Failed to fetch proxy addresses. Status code: {response.status_code}")
        return None
    
def start_browser(proxy_server_url, target_url, exit_flag, driver_instances):
    global driver_instances_lock
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f'--proxy-server={proxy_server_url}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(target_url)

    with driver_instances_lock:
        driver_instances.append(driver)

    while not exit_flag.is_set():
        time.sleep(1)

    driver.quit()

def arrange_windows(driver_list):
    screen_width = 1920  # Adjust according to your screen's resolution
    screen_height = 1080  # Adjust according to your screen's resolution

    num_windows = len(driver_list)
    columns = math.ceil(math.sqrt(num_windows))
    rows = math.ceil(num_windows / columns)

    window_width = screen_width // columns
    window_height = screen_height // rows

    for index, driver in enumerate(driver_list):
        x_position = (index % columns) * window_width
        y_position = (index // columns) * window_height
        driver.set_window_size(window_width, window_height)
        driver.set_window_position(x_position, y_position)

def check_for_exit(exit_flag):
    while True:
        user_input = input("Press 'Q' to exit: ")
        if user_input.lower() == 'q':
            exit_flag.set()
            break

if __name__ == "__main__":
    proxy_addresses = get_proxy_addresses()

    if proxy_addresses:
        proxies = proxy_addresses[:NUM_PROXIES_TO_FETCH]

        threads = []
        exit_flag = threading.Event()
        driver_instances = []

        # Start Chromium instances and store driver references
        for proxy in proxies:
            t = threading.Thread(target=start_browser, args=(proxy, TARGET_URL, exit_flag, driver_instances), name=f't{proxy}')
            t.start()
            threads.append(t)

        # Start a thread to check for exit command
        exit_thread = threading.Thread(target=check_for_exit, args=(exit_flag,))
        exit_thread.start()

        # Wait until driver_instances is populated with the expected number of instances
        while len(driver_instances) < NUM_PROXIES_TO_FETCH:
            time.sleep(1)

        # Arrange windows in a grid
        arrange_windows(driver_instances)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Wait for the exit thread to finish
        exit_thread.join()
    else:
        print("Exiting program due to failure in fetching proxy addresses.")
