from __future__ import print_function
from datetime import datetime, timedelta, timezone
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = "pycon.kr_kqq23dm5339ohe87gmuavtqnrc@group.calendar.google.com"


def slack_noti_pythonia(diff_sec) -> str:
    # 감시주기가 30분 간격으로 정해진 조건
    if 900 <= diff_sec < 2700:  # 1시간
        return '1시간 후 시작'
    elif 2700 <= diff_sec < 4500:  # 2시간
        return '2시간 후 시작'
    elif 41400 <= diff_sec < 43200:  # 1일
        return '1일 후 시작'
    else:
        return None


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)

    now_dt = datetime.now(timezone.utc)
    # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=52)
    # tomorrow = today + timedelta(days=2)

    start_time = today.isoformat() + 'Z'
    end_time = tomorrow.isoformat() + 'Z'

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=CALENDAR_ID,
                                          timeMin=start_time,
                                          timeMax=end_time,
                                          timeZone=KST,
                                          maxResults=10,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_datetime = datetime.fromisoformat(start)
        print(start, event['summary'])
        diff_time = event_datetime - now_dt
        if slack_noti_pythonia(diff_time.seconds):
            ## Add slack noti
            return


if __name__ == '__main__':
    main()
