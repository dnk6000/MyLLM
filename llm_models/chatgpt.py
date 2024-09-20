import httpx
from openai import OpenAI, BadRequestError
from config import OPENAI_API_KEY, OPENAI_PROXY

models_names = {'ChatGPT-3.5': 'gpt-3.5-turbo', 'ChatGPT-4o': 'gpt-4o'}

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_PROXY is None or OPENAI_PROXY == "" \
                 else OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client(proxy=OPENAI_PROXY))

def ask_openai(messages, model="gpt-3.5-turbo", system_prompt=None, temperature=0.7, max_tokens=150):
    try:
        response = client.chat.completions.create(
            model=models_names[model],
            messages=messages,
            temperature=temperature,   # Управление креативностью
            max_tokens=max_tokens,     # Ограничение длины ответа
        )

        return response.choices[0].message.content

    except BadRequestError as e:
        return f"Ошибка OpenAI: {str(e)}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
