import os
import sys
import requests
from datetime import datetime
WEB_HOOK_URL = os.environ["SLACK_WEB_HOOK"]
PYCON_ICON_URL = os.environ["PYCON_ICON_URL"]
# FIXME: This url will use google api call and generate document automatically
PYCON_WEEKLY_DOC_URL = os.environ["PYCON_WEEKLY_DOC_URL"]
NOW_TS = datetime.now().timestamp()


def main():
    noti_2day_ago()


def send_slack_message(slack_data):
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(WEB_HOOK_URL, json=slack_data, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def noti_2day_ago():
    if datetime.now().weekday() != 0:
        print('Notify only Monday')
        return
    title = (f'{"내일 회의 있는 날이에요!"}')
    message = (f'{":arrow_right: 참여가 가능해요 :o:"}\n'
               f'{":arrow_right: 참여가 힘들어요 :x:"}\n'
               f'{" "}\n'
               f'{"  더불어 오늘 이야기하고 싶으신 내용이 있다면"}\n'
               f'{"  회의록에 먼저 작성해주세요~ :wink:"}\n'
               f'{" "}\n'
               )
    slack_data = {
        "username": "정기회의",
        "icon_emoji": ":meow_wow:",
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
                        "text": {
                            "type": ":memo: 회의록",
                            "text": "link",
                            },
                        "style": "primary",
                        "url": PYCON_WEEKLY_DOC_URL,
                    }
                ],
                # "image_url": "xxxxxxxxxxx",  # 메시지 하단의 미리보기 image
                # "thumb_url": "xxxxxxxxxxx",  # title 옆에 이미지 보임
                # "footer": "PyconKR",
                # "footer_icon": PYCON_ICON_URL,
                "ts": NOW_TS
            }
        ]
    }
    send_slack_message(slack_data)


if __name__ == '__main__':
    main()
