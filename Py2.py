from __future__ import print_function

import datetime

import pickle

import os.path

import csv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

day = {
    'MO' : 0,
    'TU' : 1,
    'WE' : 2,
    'TH' : 3,
    'FR' : 4,
    'SA' : 5,
    'SU' : 6
}

today = datetime.datetime.today()
d2 = today.strftime("%Y-%m-%dT")
d3 = today.strftime("%Y") + '-08-01T'
print(d3)

def start_date(dates):
    num = day[dates[:2]] - today.weekday()
    if num >= 0:
        if int(d2[8:10]) < 10:
            time1 = d2[:8] + '0' + str(int(d2[8:10]) + num) + d2[10:]
            return time1
        else:
            time1 = d2[:8] + str(int(d2[8:10]) + num) + d2[10:]
            return time1
    else:
        num+=7
        if int(d2[0][8:10]) < 10:
            time1 = d2[:8] + '0' + str(int(d2[8:10]) + num) + d2[10:]
            return time1
        else:
            time1 = d2[:8] + str(int(d2[8:10]) + num) + d2[10:]
            return time1

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_time(dates, time):
    time1 = ['', '']
    d1 = start_date(dates)
    n = 0
    time3 = ''
    for x in time:
        if x == ' ':
            n+=1
        if n == 0:
            time3 += x
    time3 = str(int(time3) + 7)
    if int(time3) < 10 and (int(time3) + n) < 10:
        time1[0] = d1 + '0' + time3 + ':00:00'
        time1[1] = d1 + '0' + str(int(time3) + n) + ':50:00'
        return time1
    elif int(time3) < 10 and int(time3)+n >= 10:
        time1[0] = d1 + '0' + time3 + ':00:00'
        time1[1] = d1 + str(int(time3) + n) + ':50:00'
        return time1
    elif int(time3) >= 10 and (int(time3) + n) >= 10:
        time1[0] = d1 + time3 + ':00:00'
        time1[1] = d1 + str(int(time3) + n) + ':50:00'
        return time1



def main():
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

    with open('my_course_info.csv', mode='r') as my_course_info:
        course_reader = csv.reader(my_course_info)
        for row in course_reader:
            if row:
                summ = row[1] + ' ' + row[8] + row[2]
                loc = row[4]
                etime = ''
                if d2 > d3:
                    etime = today.strftime("%Y") + '1130'
                else:
                    etime = today.strftime("%Y") + '0430'
                rule = 'RRULE:FREQ=WEEKLY;BYDAY=' + row[5] + ';UNTIL=' + etime + ';'
                time = get_time(row[5], row[6])
                # Call the Calendar API
                event = {
                    'summary': summ,
                    'location': loc,
                    'start': {
                        'dateTime': time[0],
                        'timeZone': 'UTC+05:30',
                    },
                    'end': {
                        'dateTime': time[1],
                        'timeZone': 'UTC+05:30',
                    },
                    'recurrence': [
                        rule
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'popup', 'minutes': '20'},
                        ],
                    },
                }

                event = service.events().insert(calendarId='primary', body=event).execute()
    my_course_info.close()

if __name__ == '__main__':
    main()