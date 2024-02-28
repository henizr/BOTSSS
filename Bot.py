from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tokens import TOKEN
from task import Task

bot = TeleBot(TOKEN)
BUTTONS = ['new task', 'show todo list']
todo_list = list()

def add_new_task(message):
    bot.send_message(
        message.chat.id,
        "Enter the name of your task: "
    )

def show_todo_list(message):
    text_list = ''

    if len(todo_list) == 0:
        text_list = "Your todo list is empty"
    else:
        for i, item in enumerate(todo_list):
            text_list += f"Task #{i + 1}: {item.name}\n"

    bot.send_message(
        message.chat.id,
        text_list
    )

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
    
@bot.message_handler(commands=['newtask'])
def new_task_wrap(message):
    add_new_task(message=message)

@bot.message_handler(commands=['todolist'])
def todo_list_wrap(message):
    show_todo_list(message=message)

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == BUTTONS[0]:
        add_new_task(message = message)
    elif message.text == BUTTONS[1]:
        show_todo_list(message=message)
    else:
        new_task = Task(message.text)
        todo_list.append(new_task)
        bot.send_message(
            message.chat.id,
            f"Added a new task named '{new_task.name}'"
        )

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Вот список доступных команд:\n"
        "/start - начало работы\n/help - список доступных команд\n"
        "/new_task - добавить новую задачу\n"
        "/todo_list - посмотреть список дел"
        )

bot.polling(non_stop=True, interval=0)

