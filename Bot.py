import telebot
import json
from datetime import datetime

TOKEN = '8365813259:AAHxqK_0-YF1fIG5O-6zzngZRhHi8bFoZFk'
bot = telebot.TeleBot(TOKEN)

workouts = {}
FILE_NAME = 'workouts.json'

# Загружаем данные при запуске
def load_data():
    global workouts
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            workouts = json.load(f)
    except FileNotFoundError:
        workouts = {}

# Сохраняем данные в файл
def save_data():
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(workouts, f, ensure_ascii=False, indent=2)

load_data()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я твой дневник тренировок!\n\n"
        "/add - Добавить\n"
        "/list - История\n"
        "/count - Статистика"
    )

@bot.message_handler(commands=['add'])
def add_workout(message):
    msg = bot.send_message(message.chat.id, "Что ты тренировал?")
    bot.register_next_step_handler(msg, save_workout)

def save_workout(message):
    user_id = str(message.from_user.id)
    workout_text = message.text

    if user_id not in workouts:
        workouts[user_id] = []

    workout_entry = {
        'text': workout_text,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    }
    workouts[user_id].append(workout_entry)
    save_data()

    bot.send_message(message.chat.id, f"✅ Сохранено!\n{workout_text}")

@bot.message_handler(commands=['list'])
def list_workouts(message):
    user_id = str(message.from_user.id)

    if user_id not in workouts or len(workouts[user_id]) == 0:
        bot.send_message(message.chat.id, "Нет тренировок")
        return

    text = "📖 История:\n\n"
    for i, w in enumerate(workouts[user_id], 1):
        text += f"{i}. {w['text']}\n   {w['date']}\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['count'])
def count_workouts(message):
    user_id = str(message.from_user.id)
    count = len(workouts.get(user_id, []))
    bot.send_message(message.chat.id, f"Всего: {count} тренировок!")

print("Бот запущен!")
bot.infinity_polling()