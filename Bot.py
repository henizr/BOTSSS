from telebot import TeleBot

TOKEN = "7043913884:AAFg5FLvZeD9_VQbqcuFsmrnxuOZFnpk_d0"
bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Hi! Type 'new task' if you want to create a new task.")


bot.polling(non_stop=True, interval=0)

