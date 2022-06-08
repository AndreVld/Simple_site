import requests
from simple_site.settings import env


# sending message to telegram

def send_telegram(text: str):
    token = env('tm_BOT_TOKEN')
    channel_id = env('tm_CHAT_ID')
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    requests.post(url, data={
        "chat_id": channel_id,
        "text": text
    })
