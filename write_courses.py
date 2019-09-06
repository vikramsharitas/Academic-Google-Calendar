import csv


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


def get_courses(course, row1):
    course[2] = row1[2]  # copying number of L, P or T
    course[3] = row1[3]  # copying instructor name
    course[4] = row1[4]  # copying room no.
    course[5] = get_days(row1[5])  # copying days in correct format
    course[6] = row1[6]  # copying times
    return course


def main():
    with open('my_course_info.csv', mode='w') as my_course_info:  # writing all info onto final file
        course_writer = csv.writer(my_course_info)
        with open('course_info.csv', mode='r') as course_info:
            my_courses = csv.reader(course_info)
            for row in my_courses:
                if row:
                    with open('timetable.csv', mode='r') as timetable:
                        courses = csv.reader(timetable)
                        course = ['', '', '', '', '', '', '', '', '', '']
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
                                            course = get_courses(course, row1)
                                            course[8] = 'L'
                                            course[9] = '1'
                                            course_writer.writerow(course)
                                            c = 1
                                elif row[1] == 'P' and ('Practical' in row1 or b == 1):
                                    if 'Practical' in row1:
                                        b = 1
                                    if row[2] == row1[2]:
                                        course = get_courses(course, row1)
                                        course[8] = 'P'
                                        course[9] = '1'
                                        course_writer.writerow(course)
                                        break
                                elif row[1] == 'T' and ('Tutorial' in row1 or b == 1):
                                    if 'Tutorial' in row1:
                                        b = 1
                                    if row[2] == row1[2]:
                                        course = get_courses(course, row1)
                                        course[8] = 'T'
                                        course[9] = '1'
                                        course_writer.writerow(course)
                                        break
                                elif row[1] == '':
                                    course = get_courses(course, row1)
                                    course[8] = 'P'
                                    course [9] = '1'
                                    course_writer.writerow(course)
                                    break
                    timetable.close()
        course_info.close()
    my_course_info.close()


if __name__ == '__main__':
    main()
