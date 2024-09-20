import telebot
from telebot import types
from llm_models import chatgpt, yandex_gpt, gigachat
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения выбранной модели и контекста пользователя
user_data = {}


# Стартовая команда
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {
        'model': None,
        'system_prompt': '',
        'history': []  # Добавляем историю сообщений
    }

    bot.send_message(chat_id, "Привет! Выбери через меню модель, с которой хочешь общаться:")
    show_menu(message)


# Меню с выбором модели и другими опциями
def show_menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ChatGPT-3.5")
    btn2 = types.KeyboardButton("ChatGPT-4o")
    btn3 = types.KeyboardButton("YandexGPT")
    btn4 = types.KeyboardButton("GigaCHAT")
    btn5 = types.KeyboardButton("Установить системный промпт")
    btn6 = types.KeyboardButton("Очистить историю")  # Новая кнопка
    markup.add(btn1, btn2, btn3, btn4)
    markup.add(btn5, btn6)

    bot.send_message(chat_id, "Выберите модель:", reply_markup=markup)


# Обработка выбора модели
@bot.message_handler(func=lambda message: message.text in ["ChatGPT-3.5", "ChatGPT-4o", "YandexGPT", "GigaCHAT"])
def select_model(message):
    chat_id = message.chat.id
    selected_model = message.text
    user_data[chat_id]['model'] = selected_model
    user_data[chat_id]['history'] = [get_dict_system_prompt(chat_id,user_data[chat_id]['system_prompt'])]
    bot.send_message(chat_id, f"Модель {selected_model} выбрана. История очищена. Системный промт сохранен. Теперь можешь начать общение.")


# Установка системного промпта
@bot.message_handler(func=lambda message: message.text == "Установить системный промпт")
def set_system_prompt(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите системный промпт:")
    bot.register_next_step_handler(msg, save_system_prompt)


def save_system_prompt(message):
    chat_id = message.chat.id
    user_data[chat_id]['system_prompt'] = message.text
    user_data[chat_id]['history'][0] = get_dict_system_prompt(chat_id, message.text)
    bot.send_message(chat_id, "Системный промпт установлен.")

def get_dict_system_prompt(chat_id, prompt):
    model = user_data[chat_id]['model']
    if model == "ChatGPT-3.5" or model == "ChatGPT-4o":
        return {'role': 'system', 'content': prompt}
    elif model == "YandexGPT":
        return {'role': 'system', 'text': prompt}
    elif model == "GigaCHAT":
        return {'role': 'system', 'content': prompt}


def get_dict_user_prompt(chat_id, prompt):
    model = user_data[chat_id]['model']
    if model == "ChatGPT-3.5" or model == "ChatGPT-4o":
        return {'role': 'user', 'content': prompt}
    elif model == "YandexGPT":
        return {'role': 'user', 'text': prompt}
    elif model == "GigaCHAT":
        return {'role': 'user', 'content': prompt}

def get_dict_assistant_prompt(chat_id, prompt):
    model = user_data[chat_id]['model']
    if model == "ChatGPT-3.5" or model == "ChatGPT-4o":
        return {"role": "assistant", "content": prompt}
    elif model == "YandexGPT":
        return {'role': 'assistant', 'text': prompt}
    elif model == "GigaCHAT":
        return {'role': 'assistant', 'content': prompt}


# **Обработка команды очистки истории**
@bot.message_handler(func=lambda message: message.text == "Очистить историю")
def clear_history(message):
    chat_id = message.chat.id
    user_data[chat_id]['history'] = [get_dict_system_prompt(chat_id, user_data[chat_id]['system_prompt'])]
    bot.send_message(chat_id, "Все забыл!")


# Обработка текстовых сообщений для выбранной модели
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        # Если пользователь не запустил команду /start
        bot.send_message(chat_id, "Пожалуйста, начните с команды /start.")
        return

    if user_data[chat_id]['model'] is None:
        bot.send_message(chat_id, "Сначала выберите модель.")
        show_menu(message)
        return

    model = user_data[chat_id]['model']
    system_prompt = user_data[chat_id].get('system_prompt')
    user_message = message.text

    user_data[chat_id]['history'].append(get_dict_user_prompt(chat_id, user_message))

    history = user_data[chat_id]['history']

    response_text = 'model undefined'
    if model == "ChatGPT-3.5" or model == "ChatGPT-4o":
        response_text = chatgpt.ask_openai(history, model=model, system_prompt=system_prompt)
    elif model == "YandexGPT":
        response_text = yandex_gpt.ask_yandex_gpt(history, system_prompt)
    elif model == "GigaCHAT":
        response_text = gigachat.ask_gigachat(history, system_prompt)

    bot.send_message(chat_id, response_text)

    # Добавляем ответ бота в историю
    user_data[chat_id]['history'].append(get_dict_assistant_prompt(chat_id, response_text))


bot.polling()
