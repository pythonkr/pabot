#!/usr/bin/env python
from __future__ import print_function
import datetime
import sys, os
import json
from pathlib import Path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

# If modifying these scopes, delete the file token.json.
SCOPES = [
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
]

CALENDAR_ID="pycon.kr_kqq23dm5339ohe87gmuavtqnrc@group.calendar.google.com"
FILE_TOKEN_JSON="driveapi-327215-020a219d4cd3.json"

ENV_KEY="GOOGLE_SERVICE_ACCOUNT_JSON_KEY"


def main():
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(TOKEN_JSON, SCOPES)
    if ENV_KEY in os.environ:
        service_account_info = json.loads(os.environ[ENV_KEY])
    else:
        if os.path.exists(FILE_TOKEN_JSON):
            service_account_info = json.load(open(FILE_TOKEN_JSON))
        else:
            print("GOOGLE_TOKEN_SHOULD EXIST")
            sys.exit(1)
    #credentials = service_account.Credentials.from_service_account_file(FILE_TOKEN_JSON, scopes=SCOPES)
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + datetime.timedelta(days=2)

    start_time = today.isoformat() + 'Z'
    end_time = tomorrow.isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=CALENDAR_ID,
                                     timeMin=start_time,
                                     timeMax=end_time,
                                     timeZone=KST,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # event example
    """
    {'created': '2021-11-14T06:48:44.000Z',
 'creator': {'email': 'ding@pycon.kr'},
 'end': {'dateTime': '2021-11-14T17:00:00+09:00', 'timeZone': 'Asia/Seoul'},
 'etag': '"327020000"',
 'eventType': 'default',
 'htmlLink': 'https://www.google.com/calendar/event?eid=NThwM2MwM2ZyMXV2MzBldGlvcDd1N20xbWYgcHljb24ua3Jfa3FxMjNkbTUzMzlvaGU4N2dtdWF2dHFucmNAZw&ctz=Asia/Seoul',
 'iCalUID': '5tiop7u7m1mf@google.com',
 'id': '58p3c0om1mf',
 'kind': 'calendar#event',
 'organizer': {'displayName': 'PyCon Korea',
               'email': 'pynrc@group.calendar.google.com',
               'self': True},
 'reminders': {'useDefault': True},
 'sequence': 1,
 'start': {'dateTime': '2021-11-14T16:30:00+09:00', 'timeZone': 'Asia/Seoul'},
 'status': 'confirmed',
 'summary': '정기회의테스트 캘린더',
 'transparency': 'transparent',
 'updated': '2021-11-14T06:49:00.510Z'}"""

    if not events:
        print('No upcoming events found.')
        sys.exit()
    # store on data directory
    calendar_json_dump_file = Path("../data/calendar.json")
    json.dump(events, open(calendar_json_dump_file,"w"))


if __name__ == '__main__':
    main()
