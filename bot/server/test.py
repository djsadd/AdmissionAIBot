import requests

url = "http://127.0.0.1:8000/ask_ai/"

payload = {
    "query": "Привет, как дела?",
    "platform": "Whatsapp"  # или "Telegram"
}

response = requests.post(url, json=payload)

print("Статус:", response.status_code)
print("Ответ:", response.json())
