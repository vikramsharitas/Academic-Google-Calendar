import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
def headless_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': dir_path
        }
    }
    driver.execute("send_command", params)

options = webdriver.ChromeOptions()
# options.add_argument(
#    "user-data-dir=C:\\Users\\Vikram's Laptop\\AppData\\Local\\Google\\Chrome\\User Data") # change to profile path
options.add_argument(
    "user-data-dir=" + dir_path + '/chrome')
prefs = {"download.default_directory": dir_path}
options.add_experimental_option('prefs', prefs)
options.headless = True
driver = webdriver.Chrome('chromedriver.exe', options=options)
headless_download(driver)
driver.get(
    'https://console.developers.google.com/henhouse/?pb=%5B%22hh-0%22,%22calendar%22,null,%5B%5D,%22https:%2F%2Fdevelopers.google.com%22,null,%5B%5D,null,%22Enable%20the%20Google%20Calendar%20API%22,1,null,%5B%5D,false,false,null,null,null,null,false,null,false,false,null,null,null,%22OTHER%22,null,%22Quickstart%22,true,%22Quickstart%22,null,null,false%5D')
WebDriverWait(driver, 30).until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/hen-flow/div/hen-success-page/div[2]/div[2]/ng-container/div/a')))
driver.find_element_by_xpath('/html/body/hen-flow/div/hen-success-page/div[2]/div[2]/ng-container/div/a').click()
down = True
while down:
    time.sleep(1)
    for name in os.listdir(dir_path):
        if name == 'credentials.json':
            down = False
driver.close()