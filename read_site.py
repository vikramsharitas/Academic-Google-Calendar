from __future__ import print_function

import csv
import sys
from typing import Union

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QLabel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def write_courses(classes):
    # writing info onto csv file
    with open('course_info.csv', mode='w') as course_info:
        lec = 'l'
        for x in classes:
            # segregating based on course no. and type of class(info is of the form course no.-type of class
            y = 8
            if x.text[y] != '-':
                if x.text[y + 1] == '-':
                    y += 1
                elif x.text[y + 2] == '-':
                    y += 1
                else:
                    y -= 1
            if x.text[y + 1] == 'L' or x.text[y + 1] == 'T' or x.text[y + 1] == 'P':
                course_writer = csv.writer(course_info)
                if x.text[y + 1] == 'L':
                    lec = x.text[:y]
                    # condition for lab without lecture
                if x.text[y + 1] == 'P' and x.text[:y] != lec[:y]:
                    # in case lecture number >= 10
                    if x.text[y + 3] == '1' or x.text[y + 3] == '2' or x.text[y + 3] == '0':
                        course_writer.writerow([x.text[:y], '', x.text[y + 2:y + 4]])
                    else:
                        course_writer.writerow([x.text[:y], '', x.text[y + 2]])
                else:
                    if x.text[y + 3] == '1' or x.text[y + 3] == '2' or x.text[y + 3] == '0':
                        course_writer.writerow([x.text[:y], x.text[y + 1], x.text[y + 2:y + 4]])
                    else:
                        course_writer.writerow([x.text[:y], x.text[y + 1], x.text[y + 2]])
    course_info.close()


class App(QWidget):
    __passwd: str
    __username: str
    button: Union[QPushButton, QPushButton]
    _password_lineedit: Union[QLineEdit, QLineEdit]
    _user_lineedit: Union[QLineEdit, QLineEdit]

    def __init__(self):
        super().__init__()
        self.title = 'Academic Calendar'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox

        user_label = QLabel("Username:", self)
        user_label.move(0, 0)
        self._user_lineedit = QLineEdit(self)
        self._user_lineedit.move(100, 0)

        password_label = QLabel("Password:", self)
        password_label.move(0, 50)
        self._password_lineedit = QLineEdit(self)
        self._password_lineedit.setEchoMode(QLineEdit.Password)
        self._password_lineedit.move(100, 50)

        self.button = QPushButton('Submit', self)
        self.button.setToolTip('Submit Username and Password')
        self.button.move(100, 100)
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.__username = self._user_lineedit.text()
        self.__passwd = self._password_lineedit.text()
        self.close()

    def get_uname(self):
        return self.__username

    def get_passwd(self):
        return self.__passwd


# initiate chrome driver
def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
    username = ex.get_uname()
    passwd = ex.get_passwd()
    # username = app.get_uname()
    # passwd = app.get_passwd()
    options = Options()

    options.headless = True
    driver = webdriver.Chrome('C:\\chromedriver.exe', options=options)
    # open erp
    driver.get('http://10.2.102.21:9000/psp/hcsprod/?cmd=login&languageCd=ENG')
    # logging in
    # username = input('UserID: ')
    driver.find_element_by_id('userid').send_keys(username)
    # passwd = getpass.getpass()
    driver.find_element_by_id('pwd').send_keys(passwd)
    # navigating to page containing required info
    driver.find_element_by_name('Submit').click()
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "fldra_CO_EMPLOYEE_SELF_SERVICE")))
    driver.find_element_by_id('fldra_CO_EMPLOYEE_SELF_SERVICE').click()
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="crefli_HC_SSS_STUDENT_CENTER"]/a')))
    driver.find_element_by_xpath('//*[@id="crefli_HC_SSS_STUDENT_CENTER"]/a').click()
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ptifrmtgtframe"]')))
    iframe = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
    driver.switch_to.frame(iframe)
    # getting elements containing required info
    classes = driver.find_elements_by_class_name('PSHYPERLINKDISABLED')
    write_courses(classes)
    # close chrome driver
    driver.quit()


if __name__ == '__main__':
    main()
