import telebot
from telebot import types

TOKEN = ''  # приватные данные ^^
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Команды")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Список команд: \n"
                          "1. /makeadmin (в ответ на сообщение пользователя). Сделать админом \n"
                          "2. /ban (в ответ на сообщение пользователя). Забанить \n"
                          "3. /stat. Статистика по чату: сколько людей и админов. \n".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.reply_to_message is not None:
        bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.send_message(message.chat.id,
                         text="@{} забанен".format(message.reply_to_message.from_user.username))


@bot.message_handler(commands=['makeadmin'])
def makeadmin(message):
    if message.reply_to_message is not None:
        bot.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        bot.send_message(message.chat.id,
                         text="@{} повышен до админа".format(message.reply_to_message.from_user.username))


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Команды":
        bot.send_message(message.chat.id, text="Салам, {0.first_name}! Список команд: \n"
                                               "1. /makeadmin username. Сделать username админом \n"
                                               "2. /ban username. Забанить username \n"
                                               "3. /stat. Статистика по чату: сколько людей и админов. \n".format(
            message.from_user))
    elif message.text == "/stat":
        for x in bot.get_chat_administrators(message.chat.id):
            print(x)
        bot.send_message(message.chat.id,
                         text="Кол-во участнков: {}\n"
                              "Кол-во админов: {}".format(bot.get_chat_members_count(message.chat.id),
                                                          len(bot.get_chat_administrators(message.chat.id))))


bot.polling(none_stop=True, interval=0)
