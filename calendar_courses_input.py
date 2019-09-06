from __future__ import print_function

import csv
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

day = {
    'MO': 0,
    'TU': 1,
    'WE': 2,
    'TH': 3,
    'FR': 4,
    'SA': 5,
    'SU': 6
}
month1 = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

today = datetime.datetime.today()
d2 = today.strftime("%Y-%m-%d")
d3 = today.strftime("%Y") + '-08-01T'


def put_date(year, month, date):
    if month < 10:
        if date < 10:
            time1 = str(year) + '-0' + str(month) + '-0' + str(date) + 'T'
            print(time1)
            return time1
        else:
            time1 = str(year) + '-0' + str(month) + '-' + str(date) + 'T'
            print(time1)
            return time1
    else:
        if date < 10:
            time1 = str(year) + '-' + str(month) + '-0' + str(date) + 'T'
            print(time1)
            return time1
        else:
            time1 = str(year) + '-' + str(month) + '-' + str(date) + 'T'
            print(time1)
            return time1


def get_date(dates):
    num = day[dates[:2]] - today.weekday()
    num += 7
    date = int(d2[8:])
    month = int(d2[5:7])
    year = int(d2[:4])
    if date + num > month1[month]:
        if month == 12:
            year += 1
            month = 1
            date += num - 31
        elif month == 2:
            if year % 4 == 0:
                month += 1
                date += num - 29
            else:
                month += 1
                date += num - 28
        else:
            date += num - month1[month]
            month += 1
    else:
        date += num
    return put_date(year, month, date)


def get_time(dates, time):
    time1 = ['', '']
    d1 = get_date(dates)
    n = 0
    time3 = ''
    for x in time:
        if x == ' ':
            n += 1
        if n == 0:
            time3 += x
    time3 = (int(time3) + 7)
    if time3 < 10 and (time3 + n) < 10:
        time1[0] = d1 + '0' + str(time3) + ':00:00'
        time1[1] = d1 + '0' + str(time3 + n) + ':50:00'
        return time1
    elif time3 < 10 and (time3 + n) >= 10:
        time1[0] = d1 + '0' + str(time3) + ':00:00'
        time1[1] = d1 + str(time3 + n) + ':50:00'
        return time1
    elif time3 >= 10 and (time3 + n) >= 10:
        time1[0] = d1 + str(time3) + ':00:00'
        time1[1] = d1 + str(time3 + n) + ':50:00'
        return time1


def get_service():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def put_event(deets):
    # Call the Calendar API
    service = get_service()
    event = {
        'summary': deets[0],
        'location': deets[1],
        'start': {
            'dateTime': deets[2],
            'timeZone': 'UTC+05:30',
        },
        'end': {
            'dateTime': deets[3],
            'timeZone': 'UTC+05:30',
        },
        'recurrence': [
            deets[4]
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': '20'},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()


def get_deets():
    deets = ['', '', '', '', '']
    with open('my_course_info.csv', mode='r') as my_course_info:
        course_reader = csv.reader(my_course_info)
        for row in course_reader:
            if row:
                deets[0] = row[1] + ' ' + row[8] + row[2]
                deets[1] = row[4]
                if d2 > d3:
                    etime = today.strftime("%Y") + '1130'
                else:
                    etime = today.strftime("%Y") + '0430'
                deets[4] = 'RRULE:FREQ=WEEKLY;BYDAY=' + row[5] + ';UNTIL=' + etime + ';'
                time = get_time(row[5], row[6])
                deets[2] = time[0]
                deets[3] = time[1]
                put_event(deets)
    my_course_info.close()


def main():
    get_deets()


if __name__ == '__main__':
    main()
