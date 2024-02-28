from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tokens import TOKEN
from task import Task

bot = TeleBot(TOKEN)
BUTTONS = ['new task', 'todo list']
todo_list = list()

@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    new_task_btn = KeyboardButton(BUTTONS[0])
    to_do_list_btn = KeyboardButton(BUTTONS[1])

    markup.row(
        new_task_btn, 
        to_do_list_btn
        )

    bot.send_message(message.chat.id,
                     "Hi!\nType 'new task' if you want to create a new task.\n"
                     "Type 'todo list' if you want to look through your list todo.",
                     reply_markup=markup)

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == BUTTONS[0]:
        bot.send_message(
                        message.chat.id,
                        "Enter the name of you task:")
    elif message.text == BUTTONS[1]:
        text_list = ''
        
        for i, item in enumerate(todo_list):
            text_list += f"Task #{i + 1}: {item.name}\n"
        
        bot.send_message(
            message.chat.id,
            text_list
        )
    else:
        new_task = Task(message.text)
        todo_list.append(new_task)
        bot.send_message(
            message.chat.id,
            f"Added a new task named '{new_task.name}'"
        )

bot.polling(non_stop=True, interval=0)

