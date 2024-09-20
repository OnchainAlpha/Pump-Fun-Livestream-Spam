from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import undetected_chromedriver as uc

from random import uniform
import time



site_url = 'https://pump.fun/board'

def setup_chromedriver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=chrome_options)
    return driver


driver = setup_chromedriver()

driver.find_element(By.CSS_SELECTOR, '[type="button"][role="combobox"][aria-label="Sort"]').click()