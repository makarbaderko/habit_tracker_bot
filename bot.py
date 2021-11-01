import telebot
import config

bot = telebot.TeleBot(config.TELEGRAM_API_KEY)

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, "Здравствуйте! Я - бот🤖, позволяющий Вам отслеживать привычки!.")
    bot.send_message(message.chat.id, "Сколько привычек вы бы хотели отслеживать (до 5-и)")
    bot.register_next_step_handler(msg, count_habits)
def count_habits(message):
    global n_habits
    if message.text.isnumeric():
        n_habits = int(message.text)
        msg = bot.reply_to(message, "Введите Ваши привычки, по одной на сообщение")
        global habit_list
        habit_list = []
        bot.register_next_step_handler(msg, get_habits)
    else:
        msg = bot.reply_to(message, "Это не число :) Попробуйте еще раз")
        bot.register_next_step_handler(msg, count_habits)
def get_habits(message):
    if len(habit_list)+1 < n_habits:
        habit_list.append(message.text)
        bot.register_next_step_handler(message, get_habits)
    else:
        msg = bot.reply_to(message, "Введите время, когда я должен прислать напоминание\nдля каждой привычки (в формате 24ч), например - 20:31")
        global time_list
        time_list = []
        bot.register_next_step_handler(msg, get_times)
def get_times(message):
    txt = str(message.text)
    print(txt)
    print(len(txt), txt[:2], int(txt[3:]))
    print(f": = {txt[2]}")
    if len(time_list)+1 <= n_habits:
        if len(txt) == 5 and int(txt[:2]) <= 24 and int(txt[3:]) <= 60 and txt[2] == ':':
            time_list.append(message.text)
            bot.register_next_step_handler(message, get_times)
        else:
            msg = bot.reply_to(message, "Это не время в необходимом формате :) Попробуйте еще раз")
            bot.register_next_step_handler(message, get_times)
    else:
        msg = bot.reply_to(message, "Отлично, настройка завершена!")
bot.polling()