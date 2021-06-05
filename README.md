PyConKR Arrangement Bot
=======================

Weekly meetup
-------------

### 목적
회의때마다 담당자가 교대로 슬랙에 올리기 번거롭다.
자동으로 올려지면 편리하고 좋을것 같다.

### 요구사항
알림
- 2일전에 회의가 있음을 알린다.
- 1시간 전에 곧 회의가 시작함을 알린다.
- 5분전에 곧 회의가 시작함을 알린다.

링크
- Zoom 링크는 permanent link 생성해서 일괄 처리
- Google documnet는 API를 써서 자동생성한 후 그 링크를 공유한다. (Oauth2에서 막혀있다.)

슬랙
- Webhook Url을 이용
- attachments 옵션을 이용 [매뉴얼](https://api.slack.com/messaging/composing/layouts#building-attachments) 기능이 더 필요한 경우 Block array 기능을 이용하면 될 것 같음

Reference
- Slack
-- 메시징 매뉴얼:  https://api.slack.com/messaging/composing/layouts
-- @xxx 호출    : https://slack.com/intl/en-kr/help/articles/202009646-Notify-a-channel-or-workspace
-- Attachment   : https://api.slack.com/messaging/composing/layouts#attachments

- Github
-- github actions   : https://docs.github.com/en/actions
-- setup-python 관련: https://github.com/actions/setup-python
-- schedule setup   : https://github.community/t/how-to-setup-github-actions-to-run-my-python-script-on-schedule/18335

License
-------
곧 추가
