import telebot
from tokens import (
    TOKEN
)

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    print("start")
    bot.send_message(message.chat.id,
                     text="Привет, напиши Новая задача для добавления новой задачи!")


bot.polling(
    non_stop=True,
    interval=0
)