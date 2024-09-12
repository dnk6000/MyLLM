import requests

import config


def ask_yandex_gpt(prompt, system_prompt=None):
    # Логика взаимодействия с YandexGPT API
    return "Ответ от YandexGPT: " + prompt


api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

api_key = config.YANDEX_API_KEY

headers = {
    "Authorization": f"Api-Key {api_key}",
    "Content-Type": "application/json"
}

data = {
    "modelUri": "gpt://b1g7bnjhumh84ul2i4f4/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0,
        "maxTokens": "200"
    },
    "messages": [
        {
            "role": "system",
            "text": "Исправь грамматические, орфографические и пунктуационные ошибки в тексте. Сохраняй исходный порядок слов"
        },
        {
            "role": "user",
            "text": "Нейросети помогают человеку работать быстрее и эффективнее но опосения что искуственный интелек заменит человека - пока преждевремены"
        }
    ]
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 200:
    print(response
          .json()
          .get("result")
          .get("alternatives")[0]
          .get("message")
          .get("text")
          )
else:
    print(f"Error: {response.status_code}, {response.text}")