import os
import re
import datetime
import logging
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from wakatime import WakaTime, time_setup

# Initializes your app with your bot token and socket mode handler
# /home/eunbinpark/workspace/waka-slackbot
load_dotenv(dotenv_path="./.env")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")

assert SLACK_BOT_TOKEN and SLACK_APP_TOKEN, "Missing Slack tokens"

# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
app = App(token=SLACK_BOT_TOKEN)
wk = WakaTime()


@app.event("app_mention")
def handle_app_mention_events(body, say):
    today = datetime.datetime.today()
    date = today.strftime("%m월 %d일, %H시 %M분")
    lang_times = wk.get_language_time_today().items()
    text = f":female_fairy: {date} 업무 종료 :male_fairy:\n\n금일 코드 작성 시간은 다음과 같습니다.\n"

    channel_id = body["event"]["channel"]
    event_ts = body["event"]["ts"]

    for lang, time in lang_times:
        time_formattimg = time_setup(time)
        text += f"- {lang:15} {time_formattimg}\n"

    say(text=text,
        channel=channel_id,
        thread_ts=event_ts)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
