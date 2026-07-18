
import os
import time
import requests
import json
import datetime
import dotenv
import threading

def send_unlock_request(cookie: str) -> dict | None:
    url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"

    headers = {
        "cookie": cookie,
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.12.0"
    }

    data = {
        "is_retry": True
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Request failed: {response}")
    else:
        return response.json()

def check_response(response_json: dict) -> bool:
    if response_json["code"] != 0:
        print("Login token expired. Generate a new token by following the steps on README.md.")
        print(json.dumps(response_json, indent=2))
        return False
    else:
        print("Token fresh. Can send requests...")
        print(json.dumps(response_json, indent=2))
        return True

def seconds_left_until_utc_8_midnight():
    utc_plus_8 = datetime.timezone(datetime.timedelta(hours=8))
    utc_plus_8_now = datetime.datetime.now(utc_plus_8)
    utc_plus_8_next_midnight = (utc_plus_8_now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_left = int((utc_plus_8_next_midnight - utc_plus_8_now).total_seconds())
    return seconds_left

def start_request_thread(cookie: str):
    def target():
        print("Thread started!")
        r = send_unlock_request(cookie)
        print(json.dumps(r, indent=2))
    t = threading.Thread(
        target=target,
    )
    t.start()

def unlock_retry_request(start_when_seconds_left: int, cookie: str) -> None:
    print("Making sure token is fresh...")
    r = send_unlock_request(cookie)
    if r is None:
        print("Something is wrong. You can create an issue.")
        return
    else:
        if not check_response(r):
            print("Your token is expired. Get a fresh token, preferebly do it when less than 30 minutes (1800 seconds) left.")
            return

    print(f"Waiting until {start_when_seconds_left} seconds left to UTC+8 midnight.")
    while seconds_left_until_utc_8_midnight() > start_when_seconds_left:
        print(f"  Currently {seconds_left_until_utc_8_midnight()} seconds left...\r", end="")
        time.sleep(0.1)

    print()
    print("Starting sending requests...")
    while 0 <= seconds_left_until_utc_8_midnight():
        start_request_thread(cookie)
        time.sleep(0.1)

if __name__ == "__main__":

    dotenv.load_dotenv()
    cookie = os.getenv("COOKIE")
    if cookie is None:
        print("Please set COOKIE in .env file")
        exit(1)
    else:
        unlock_retry_request(10, cookie)
