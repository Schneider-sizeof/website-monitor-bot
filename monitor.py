import requests
import time
from datetime import datetime

BOT_TOKEN = "8795470252:AAE6OecD2NFez12TtXqdfwb-TnnhPu5cAw8"
CHAT_ID = "8784265275"

WEBSITES = [
    "https://google.com",
    "https://biokiees.com",
    "https://morocco.blsspainvisa.com/?utm_source=chatgpt.com"
]

CHECK_INTERVAL = 60  # seconds

status_cache = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def check_website(url):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return "UP"
        else:
            return "DOWN"

    except:
        return "DOWN"

print("Monitoring started...")

while True:

    for site in WEBSITES:

        current_status = check_website(site)
        previous_status = status_cache.get(site)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # First check
        if previous_status is None:
            status_cache[site] = current_status
            print(f"[{timestamp}] {site} => {current_status}")

        # Status changed
        elif previous_status != current_status:

            if current_status == "DOWN":
                message = f"🚨 WEBSITE DOWN\n\n{site}\n\nTime: {timestamp}"

            else:
                message = f"✅ WEBSITE BACK ONLINE\n\n{site}\n\nTime: {timestamp}"

            send_telegram_message(message)

            print(message)

            status_cache[site] = current_status

    time.sleep(CHECK_INTERVAL)