import os
import time

from selenium import webdriver

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=" + dir_path + '/chrome')
prefs = {"download.default_directory": dir_path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options, executable_path='C:\chromedriver')
driver.get(
    'https://accounts.google.com/ServiceLogin/signinchooser?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgfe_rd%3Dcr%26ei%3DTQV1V-6cBe7I8AeU9pXwAQ%26gws_rd%3Dssl%2Ccr%26fg%3D1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
time.sleep(60)
driver.close()

#https://www.google.com/?gfe_rd=cr&ei=TQV1V-6cBe7I8AeU9pXwAQ&gws_rd=ssl,cr&fg=1
