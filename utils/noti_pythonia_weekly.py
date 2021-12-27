import os.path
import json
import sys
from requests import post
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from google.oauth2 import service_account
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
PYCON_CALENDAR_ID = os.environ["PYCON_CALENDAR_ID"]
ZOOM_LINK = os.environ["ZOOM_LINK"]
PYCON_WEEKLY_DOC_URL = os.environ["PYCON_WEEKLY_DOC_URL"]
PYCON_ICON_URL = os.environ["PYCON_ICON_URL"]
WEB_HOOK_URL = os.environ["SLACK_WEB_HOOK"]

ENV_KEY = "GOOGLE_SERVICE_ACCOUNT_JSON_KEY"
FILE_TOKEN_JSON = "driveapi-327215-020a219d4cd3.json"


def send_slack_message(slack_data):
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = post(WEB_HOOK_URL, json=slack_data, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def noti_before_hour(hour: int) -> None:
    message = (f'{"오늘 이야기하고 싶으신 내용이 있다면"}\n'
               f'{"회의록에 먼저 작성해주세요"}\n'
               f'{"혹은 오늘 회의록을 먼저 읽고 참석해주세요~ :wink:"}\n'
               )
    slack_data = {
        "username": "정기회의",
        "icon_emoji": ":pyconkr:",
        "channel": "#0-general",
        "attachments": [
            {
                "fallback": "Weekly Meetup",
                "color": "#9733EE",
                "pretext": f"<!channel> 잠시 후 20시에 회의 시작이에요!",
                "fields": [
                    {
                        "value": message,
                        "short": "false",
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": {"type": "Zoom 링크", "text": "link", },
                        "style": "primary",
                        "url": ZOOM_LINK,
                    },
                    {
                        "type": "button",
                        "text": {"type": ":memo: 회의록", "text": "link", },
                        "style": "primary",
                        "url": PYCON_WEEKLY_DOC_URL,
                    }
                ]
            }
        ]
    }
    send_slack_message(slack_data)


def noti_before_day(day: int) -> None:
    if datetime.now().weekday() != 0:
        print('Notify weekday')
        return
    title = (f'{"{day}일 후 회의 있는 날이에요!"}')
    message = (f'{":arrow_right: 참여가 가능해요 :o:"}\n'
               f'{":arrow_right: 참여가 힘들어요 :x:"}\n'
               f'{" "}\n'
               f'{"  더불어 정기회의에서 이야기하고 싶으신 내용이 있다면"}\n'
               f'{"  회의록에 먼저 작성해주세요~ :wink:"}\n'
               f'{" "}\n'
               )
    slack_data = {
        "username": "정기회의",
        "icon_emoji": ":pyconkr:",
        "channel": "#0-general",
        "attachments": [
            {
                "fallback": "파준위 정기회의",
                "color": "#F3DE63",
                "pretext": "<!channel> 회의 참여 가능 여부를 이모지로 알려주세요~",
                "author_name": "PyconKR",
                "author_link": "http://pycon.kr/",
                "author_icon": PYCON_ICON_URL,
                # "text": "--------------------------",
                # "title": ":memo: 회의록",
                # "title_link": PYCON_WEEKLY_DOC_URL,
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": {"type": ":memo: 회의록", "text": "link", },
                        "style": "primary",
                        "url": PYCON_WEEKLY_DOC_URL,
                    }
                ],
                # "image_url": "xxxxxxxxxxx",  # 메시지 하단의 미리보기 image
                # "thumb_url": "xxxxxxxxxxx",  # title 옆에 이미지 보임
                # "footer": "PyconKR",
                # "footer_icon": PYCON_ICON_URL,
                "ts": datetime.now().timestamp()
            }
        ]
    }
    send_slack_message(slack_data)


def slack_noti_pythonia(diff_hour: int, diff_sec: int) -> None:
    # 감시주기가 30분 간격으로 정해진 조건
    if diff_hour == 1:
        if 900 <= diff_sec < 2700:   # 1일
            noti_before_day(1)
    elif diff_hour == 0:
        if 900 <= diff_sec < 2700:  # 1시간
            noti_before_hour(1)
        elif 3600 <= diff_sec < 4500:  # 2시간
            noti_before_hour(2)


def main() -> None:
    if ENV_KEY in os.environ:
        service_account_info = json.loads(os.environ[ENV_KEY])
    else:
        if os.path.exists(FILE_TOKEN_JSON):
            service_account_info = json.load(open(FILE_TOKEN_JSON))
        else:
            print("GOOGLE_TOKEN_SHOULD EXIST")
            sys.exit(1)
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    now_dt = datetime.now(timezone.utc)
    # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=52)
    # tomorrow = today + timedelta(days=2)

    start_time = today.isoformat() + 'Z'
    end_time = tomorrow.isoformat() + 'Z'

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=PYCON_CALENDAR_ID,
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
        slack_noti_pythonia(diff_time.days, diff_time.seconds)


if __name__ == '__main__':
    main()
