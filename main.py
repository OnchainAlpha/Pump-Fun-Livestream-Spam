from playwright.sync_api import sync_playwright
from constants import messages, reply, image_path
from utils import get_logger
from controller import Controller
from pathlib import Path
import traceback
import subprocess
import time
import requests

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
debugging_port = '--remote-debugging-port=8989'
user_data_dir = '--user-data-dir={}'.format(Path.cwd() / 'profile')

# Function to start the browser process
def start_browser():
    subprocess.Popen([chrome_path, debugging_port, user_data_dir])
    time.sleep(3)
    ws_url = requests.get('http://127.0.0.1:8989/json/version').json()['webSocketDebuggerUrl']
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp(ws_url)
    return p, browser

# Outer loop to restart the process
while True:  
    # Start the browser
    p, browser = start_browser()
    context = browser.contexts[0]
    page = context.pages[0]
    c = Controller(page)
    logger = get_logger()

    # Go to the initial page
    page.goto('https://pump.fun/')
    start_time = time.time()  # Record the start time

    # Inner loop to repeat tasks
    while True:
        current_time = time.time()
        if current_time - start_time > 600:  # Break after 10 minutes
            logger.info("10 minutes passed. Exiting and restarting script...")
            browser.close()
            p.stop()
            break  # Exit inner loop after 10 minutes

        page.goto('https://pump.fun/')
        urls = c.get_urls()
        logger.info(f'Found urls: {len(urls)}')
        for url in urls:
            logger.info(f'Going to url: {url}')
            try:
                page.goto(url)
                page.wait_for_timeout(8000)
                c.spam_messages(messages)
                page.wait_for_timeout(2000)
                c.send_reply(reply, image_path)
                page.wait_for_timeout(8000)
            except Exception as e:
                logger.error(f'exception occurred: {e}')
                logger.error(traceback.format_exc())

    # Wait for 5 minutes before restarting the loop
    time.sleep(300)
