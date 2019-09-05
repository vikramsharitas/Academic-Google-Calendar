from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import getpass

import csv

# initiate chrome driver
driver = webdriver.Chrome('C:\\chromedriver.exe')
# open erp
driver.get('http://10.2.102.21:9000/psp/hcsprod/?cmd=login&languageCd=ENG')
# logging in
username = input('UserID: ')
driver.find_element_by_id('userid').send_keys(username)
# passwd = getpass.getpass("password: ")
passwd = 'Bits@32523'
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
# close chrome driver
driver.quit()


def get_days(row1):  # formatting days to make it usable as the way to send requests is not the way the given dta is
    y = ''
    course = ''
    n = 0
    days = {
        'M': 'MO',
        'T': 'TU',
        'W': 'WE',
        'Th': 'TH',
        'F': 'FR',
        'S': 'SA',
    }
    for x in row1:
        if x != ' ':
            y += x
        elif n == 0:
            course += days[y]
            y = ''
            n += 1
        else:
            course += ','
            course += days[y]
            y = ''
    if n == 1:
        course += ','
    course += days[y]
    return course


def get_courses(courses, row1):
    course[2] = row1[2]  # copying number of L, P or T
    course[3] = row1[3]  # copying instructor name
    course[4] = row1[4]  # copying room no.
    course[5] = get_days(row1[5])  # copying days in correct format
    course[6] = row1[6]  # copying times
    return courses


with open('my_course_info.csv', mode='w') as my_course_info:  # writing all info onto final file
    course_writer = csv.writer(my_course_info)
    with open('course_info.csv', mode='r') as course_info:
        my_courses = csv.reader(course_info)
        for row in my_courses:
            if row:
                with open('timetable.csv', mode='r') as timetable:
                    courses = csv.reader(timetable)
                    course = ['', '', '', '', '', '', '', '', '']
                    b = 0
                    n = 0
                    c = 0
                    for row1 in courses:
                        if row[0] in row1 or row[0] in course:
                            if row[0] in row1:
                                course[0] = row1[0]  # copying course no.
                                course[1] = row1[1]  # copying course name
                                course[7] = row1[7]  # copying L, P or T
                            if row[1] == 'L':
                                if c == 0:
                                    b += 1
                                    n += 1
                                else:
                                    n += 1
                                if n == (b + 1) and row1[2] == '' and row1[5] != '' and c == 1:
                                    course[5] = get_days(row1[5])
                                    course[6] = row1[6]
                                    course_writer.writerow(course)
                                    break
                                elif c == 1:
                                    break
                                else:
                                    if row[2] == row1[2]:
                                        courses = get_courses(courses, row1)
                                        course[8] = 'L'
                                        course_writer.writerow(course)
                                        c = 1
                            elif row[1] == 'P' and ('Practical' in row1 or b == 1):
                                if 'Practical' in row1:
                                    b = 1
                                if row[2] == row1[2]:
                                    courses = get_courses(courses, row1)
                                    course[8] = 'P'
                                    course_writer.writerow(course)
                                    break
                            elif row[1] == 'T' and ('Tutorial' in row1 or b == 1):
                                if 'Tutorial' in row1:
                                    b = 1
                                if row[2] == row1[2]:
                                    courses = get_courses(courses, row1)
                                    course[8] = 'T'
                                    course_writer.writerow(course)
                                    break
                            elif row[1] == '':
                                courses = get_courses(courses, row1)
                                course[8] = 'P'
                                course_writer.writerow(course)
                                break
                timetable.close()
    course_info.close()
my_course_info.close()
