from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tokens import TOKEN
from __archive.task import Task


bot = TeleBot(TOKEN)
BUTTONS = ['new task', 'show todo list']
WEEK_BUTTONS = [
    "Понедельник", 
    "Вторник", 
    "Среда", 
    "Четверг", 
    "Пятница", 
    "Суббота", 
    "Воскресенье"
    ]

TIME_START = 7
TIME_END = 21

todo_list: list[Task] = list[Task]()
keyboard_buttons: list = list()

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
            text_list += f"Task #{i + 1}: {item.name}\n task day: {item.task_day}\n\n"

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

        keyboard = InlineKeyboardMarkup(row_width=4)

        for i, day in enumerate(WEEK_BUTTONS):
            day_btn = InlineKeyboardButton(
            WEEK_BUTTONS[i], 
            callback_data= day
            )
            keyboard_buttons.append(day_btn)

        keyboard.add(*keyboard_buttons)

        bot.send_message(
            message.chat.id,
            "Choose the day of starrting your task",
            reply_markup=keyboard
        )

        keyboard_time = InlineKeyboardMarkup(row_width=5)
        keyboard_buttons_time = []
        for time in range(TIME_START, TIME_END + 1):
            time_str = f"{time}:00"
            time_btn=InlineKeyboardButton(time_str, callback_data=time_str)
            keyboard_buttons_time.append(time_btn)

        keyboard_time.add(*keyboard_buttons_time)
        bot.send_message(message.chat.id, "Выберите время начала задачи", reply_markup=keyboard_time)




@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Вот список доступных команд:\n"
        "/start - начало работы\n/help - список доступных команд\n"
        "/new_task - добавить новую задачу\n"
        "/todo_list - посмотреть список дел"
        )

@bot.callback_query_handler(func=lambda call: True)
def day_select(call):
    if len(todo_list) > 0:
        todo_list[-1].task_day = call.data

    bot.edit_message_text(
        f"Запланирована на {call.data}", 
        call.message.chat.id, 
        call.message.message_id
        )
    bot.answer_callback_query(call.id)
    print("Выбор дня")


@bot.callback_query_handler(func=lambda call: True)
def time_select(call):
    if len(todo_list) > 0:
        todo_list[-1].time = call.data
    bot.edit_message_text(f"Запланирована на {call.data}", 
                          call.message.chat.id, 
                          call.message.message_id)
    bot.answer_callback_query(call.id)

    print("Выбор времени")


bot.polling(non_stop=True, interval=0)

