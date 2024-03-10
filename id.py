import requests

def get_chat_id(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    data = response.json()
    chat_id = data["result"][0]["message"]["chat"]["id"]  # Obtener el ID del primer mensaje
    return chat_id

# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot de Telegram
bot_token = '6136271594:AAHrE2o76Fd1Bos-_tGYO-NK4WUYl3y5IqI'
chat_id = get_chat_id(bot_token)
print("ID del chat:", chat_id)
