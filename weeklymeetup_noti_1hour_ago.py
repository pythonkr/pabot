import os
import sys
import requests
from datetime import datetime
WEB_HOOK_URL = os.environ["SLACK_WEB_HOOK"]
PYCON_ICON_URL = os.environ["PYCON_ICON_URL"]
PYCON_WEEKLY_DOC_URL = os.environ["PYCON_WEEKLY_DOC_URL"]
GATHERTOWN_LINK = os.environ["GATHERTOWN_LINK"]
# ZOOM_LINK = os.environ["ZOOM_LINK"]

NOW_TS = datetime.now().timestamp()


def main():
    noti_1hour_ago()


def send_slack_message(slack_data):
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(WEB_HOOK_URL, json=slack_data, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def noti_1hour_ago():
    return
    if datetime.now().weekday() != 2:
        print('Notify only Wednesday')
        return
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
                "pretext": "<!channel> 1시간 후에 회의 시작이에요!",
                "fields": [
                    {
                        "value": message,
                        "short": "false",
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": {
                            "type": "GatherTown 링크",
                            "text": "link",
                            },
                        "style": "primary",
                        "url": GATHERTOWN_LINK,
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": ":memo: 회의록",
                            "text": "link",
                            },
                        "style": "primary",
                        "url": PYCON_WEEKLY_DOC_URL,
                    }
                ]
            }
        ]
    }
    send_slack_message(slack_data)


if __name__ == '__main__':
    main()
