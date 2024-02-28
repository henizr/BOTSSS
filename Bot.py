from telebot import TeleBot
from tokens import TOKEN

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Hi!\nType 'new task' if you want to create a new task.\n"
                     "Type 'todo list' if you want to look through your list todo.")

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == "new task":
        bot.send_message(
                        message.chat.id,
                        "Enter the name of you task:")
    if message.text == "todo list":
        bot.send_message(
                        message.chat.id,
                        "Here will be you list:")

bot.polling(non_stop=True, interval=0)

