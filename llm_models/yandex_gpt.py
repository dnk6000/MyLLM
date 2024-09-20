import requests

import config

api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

api_key = config.YANDEX_API_KEY

modelUri = f"gpt://{config.YANDEX_CATALOG}/yandexgpt/latest"

headers = {
    "Authorization": f"Api-Key {api_key}",
    "Content-Type": "application/json"
}

def ask_yandex_gpt(messages, system_prompt=None, temperature=0.7, max_tokens=150):
    data = {
        "modelUri": modelUri,
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens
        },
        "messages": messages
    }
    if messages[0].get("text") == "":
        messages[0]['text'] = 'Общайся как обычно'

    try:
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            res_text = response.json().get("result").get("alternatives")[0].get("message").get("text")
        else:
            res_text =  f"Error: {response.status_code}, {response.text} \n {messages}"
    except Exception as e:
        res_text =  f"Произошла ошибка: {str(e)}"

    return res_text


if __name__ == "__main__":
    messages = []
    messages.append({'role': 'system', 'text': 'Общайся как обычно'})
    messages.append({'role': 'user', 'text': 'Привет!'})
    messages.append({'text': 'Привет! Как дела?', 'role': 'assistant'})
    messages.append({'role': 'user', 'text': 'Расскажи про погоду в Египте?'})

    ask_yandex_gpt(messages)
