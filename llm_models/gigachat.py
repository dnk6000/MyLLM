import requests
import base64
from dotenv import set_key
from datetime import datetime
import json

import config



CLIENT_SCOPE = 'GIGACHAT_API_PERS'

def ask_gigachat(messages, system_prompt=None, temperature=0.7, max_tokens=150):
    api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {config.GIGACHAT_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if messages[0].get("content") == "":
        messages[0]['content'] = 'Общайся как обычно'

    data = {
        'model': 'GigaChat',
        'messages': messages,
        'temperature': temperature,
        'top_p': 0.1,
        'n': 1,
        'stream': False,
        'max_tokens': max_tokens,
        'repetition_penalty': 1
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            res = response.json()
            res_message = res['choices'][0]['message']
            res_text = res_message['content']
        else:
            res_text = f"Error: {response.status_code}, {response.text} "
    except Exception as e:
        res_text = f"Произошла ошибка: {str(e)}"

    return res_text


def get_token(force=False):
    if not force:
        current_time = int(datetime.now().timestamp() * 1000)
        is_token_expired = current_time >= config.GIGACHAT_TOKEN_EXPIRES
        if not is_token_expired:
            return

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    authorization_string = f"{config.GIGACHAT_CLIENT_ID}:{config.GIGACHAT_CLIENT_SECRET}"
    encoded_authorization = base64.b64encode(authorization_string.encode('utf-8')).decode()

    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efb2dc98e',
        'Authorization': f'Basic {encoded_authorization}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    data = json.loads(response.text)

    config.GIGACHAT_TOKEN = data['access_token']
    config.GIGACHAT_TOKEN_EXPIRES = data['expires_at']

    set_key(config.dotenv_path, 'GIGACHAT_TOKEN', config.GIGACHAT_TOKEN)
    set_key(config.dotenv_path, 'GIGACHAT_TOKEN_EXPIRES', str(config.GIGACHAT_TOKEN_EXPIRES))

def get_token2():
    "non-working code from lesson !!!"

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    response = requests.post(
        url,
        data={
            'grant_type': 'client_credentials',
            'client_id': config.GIGACHAT_CLIENT_ID,
            'client_secret': config.GIGACHAT_CLIENT_SECRET
        }
    )
    access_token = response.json()['access_token']
    print(access_token)

def test_via_api():
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    data = {
        'model': 'GigaChat',
        'messages': [],
        'temperature': 0.7,
        'top_p': 0.1,
        'n': 1,
        'stream': False,
        'max_tokens': 512,
        'repetition_penalty': 1
    }

    headers = {
        'Authorization': f'Bearer {config.GIGACHAT_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    while True:
        user_input = input("User: ")
        data['messages'].append({'role': 'user', 'content': user_input})

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                res = response.json()
                res_message = res['choices'][0]['message']
                res_text = res_message['content']
                data['messages'].append(res_message)
            else:
                res_text = f"Error: {response.status_code}, {response.text} "
                print(res_text)
                break
        except Exception as e:
            res_text = f"Произошла ошибка: {str(e)}"
            print(res_text)
            break

def test_via_langchain():
    """ НЕ завелось!! Пример работы с чатом через gigachain"""
    from langchain.schema import HumanMessage, SystemMessage
    from langchain_community.chat_models.gigachat import GigaChat

    # Авторизация в сервисе GigaChat
    # chat = GigaChat(credentials=config.GIGACHAT_AUTHORYTY_DATA, verify_ssl_certs = False)
    chat = GigaChat(credentials=config.GIGACHAT_TOKEN, verify_ssl_certs = False)

    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
        )
    ]

    # Запускаем бесконечный цикл
    while True:
        # Запрашиваем ввод пользователя через консоль
        user_input = input("User: ")

        hm = HumanMessage(content=user_input)


        # Добавляем сообщение пользователя в список сообщений
        messages.append(hm)

        # Отправляем список сообщений в чат и получаем ответ от бота
        res = chat(messages)

        # Добавляем ответ бота в список сообщений
        messages.append(res)

        # Выводим ответ бота на экран
        print("Bot: ", res.content)


if __name__ == "__main__":
    get_token()
    # test_via_langchain()
    # test_via_api()
