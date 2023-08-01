import os
from dotenv import load_dotenv
import base64
import requests
import datetime
from datetime import timedelta


class WakaTime:
    def __init__(self, wakatime_id="cosmos42"):
        load_dotenv()
        self.__api_key = os.getenv("WAKATIME_API_KEY", "")
        assert self.__api_key, "Missing WakaTime API key"
        self.api_base_url = "https://wakatime.com/api"
        self.wakatime_id = wakatime_id
        self.headers = self.get_headers()

    @property
    def api_key(self):
        raise Exception("Direct Access to api_key is not allowed")

    @api_key.setter
    def api_key(self, value):
        raise Exception("Direct modification of api_key is not allowed")

    def get_headers(self, user_agent=None):
        encoded_key = str(base64.b64encode(bytes(str(self.__api_key), "utf-8")), "utf-8")
        if user_agent is None:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15"
        return {
            "Authorization": f"Basic {encoded_key}",
            "User-Agent": user_agent
        }

    def get_language_time_today(self):
        url = self.api_base_url + f"/v1/users/{self.wakatime_id}/status_bar/today"
        req = requests.get(url=url, headers=self.headers)
        if req.status_code == 200:
            req_json = req.json()
            my_lang_time = {}
            for proj in req_json["data"]["languages"]:
                lang_time = datetime.timedelta(seconds=proj["total_seconds"])
                if lang_time < datetime.timedelta(seconds=10):
                    continue
                my_lang_time[proj["name"]] = str(lang_time).split(".")[0]
            return my_lang_time

        else:
            raise ("Error: " + str(req.status_code))


def time_setup(time: str):
    split_time = time.split(":")
    if split_time[0] != "0":
        return f"{split_time[0]} hrs {split_time[1]} min {split_time[-1]} sec"
    else:
        return f"{split_time[1]} min {split_time[-1]} sec"