import os
from dotenv import load_dotenv

dotenv_path = os.path.dirname(os.path.abspath(__file__))+'\\.env'

# Загружаем переменные окружения из .env файла
load_dotenv(dotenv_path)

# Считываем переменные из .env файла и сохраняем их как константы
BOT_TOKEN = os.getenv('BOT_TOKEN')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_PROXY = os.getenv('OPENAI_PROXY')

YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
YANDEX_CATALOG = os.getenv('YANDEX_CATALOG')

GIGACHAT_CLIENT_ID = os.getenv('GIGACHAT_CLIENT_ID')
GIGACHAT_CLIENT_SECRET = os.getenv('GIGACHAT_CLIENT_SECRET')
GIGACHAT_AUTHORYTY_DATA = os.getenv('GIGACHAT_AUTHORYTY_DATA')

GIGACHAT_TOKEN = os.getenv('GIGACHAT_TOKEN')
GIGACHAT_TOKEN_EXPIRES=int(os.getenv('GIGACHAT_TOKEN_EXPIRES'))
GIGACHAT_TOKEN_PERIOD_VALIDITY=int(os.getenv('GIGACHAT_TOKEN_PERIOD_VALIDITY'))
