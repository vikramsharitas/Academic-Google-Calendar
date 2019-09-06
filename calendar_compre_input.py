from __future__ import print_function

import csv
import datetime
import os
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

today = datetime.datetime.today()
d2 = today.strftime("%Y-%m-%d")
d3 = today.strftime("%Y") + '-08-01T'


def get_date(dates):
    # x = ''
    n = 0
    day = ''
    month = ''
    strtime = ''
    time = ['', 's']
    for x in dates:
        if x == ' ':
            n = 2
        elif x != '/' and n == 0:
            day += x
        elif x == '/':
            n = 1
        elif n == 1:
            month += x
        elif n == 2:
            strtime += x
    month = int(month)
    day = int(day)
    if strtime == 'AN':
        time[0] = '14:00:00'
        time[1] = '17:00:00'
    if strtime == 'FN':
        time[0] = '09:00:00'
        time[1] = '12:00:00'
    if month < 10 and day < 10:
        date = today.strftime("%Y") + '-0' + str(month) + '-0' + str(day) + 'T'
    elif month >= 10 and day < 10:
        date = today.strftime("%Y") + '-' + str(month) + '-0' + str(day) + 'T'
    elif month >= 10 and day >= 10:
        date = today.strftime("%Y") + '-' + str(month) + '-' + str(day) + 'T'
    elif month < 10 and day >= 10:
        date = today.strftime("%Y") + '-0' + str(month) + '-' + str(day) + 'T'
    time[0] = date + time[0]
    time[1] = date + time[1]
    return time


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
        'start': {
            'dateTime': deets[1],
            'timeZone': 'UTC+05:30',
        },
        'end': {
            'dateTime': deets[2],
            'timeZone': 'UTC+05:30',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': '120'},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()


def get_deets():
    deets = ['', '', '']
    course_name = ''
    with open('my_course_info.csv', mode='r') as my_course_info:
        course_reader = csv.reader(my_course_info)
        for row in course_reader:
            if row:
                if row[7] != '' and row[9] == '1':
                    deets[0] = row[1] + ' COMPRE'
                    time = get_date(row[7])
                    deets[1] = time[0]
                    deets[2] = time[1]
                    if deets[0] != course_name:
                        put_event(deets)
                        course_name = deets[0]
    my_course_info.close()


def main():
    get_deets()


if __name__ == '__main__':
    main()
