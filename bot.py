import config
import utils
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

currentMaster_id = -1;
bot.statusFL = False
bot.loginFL = False
bot.partsFL = True

@bot.message_handler(commands=["help"])
def send_help(message): 
    
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    btns.append(types.InlineKeyboardButton(text="Помощь - help", callback_data="help"))
    btns.append(types.InlineKeyboardButton(text="Свободное время", callback_data="time"))
    btns.append(types.InlineKeyboardButton(text="Статус готовности", callback_data="status"))
    btns.append(types.InlineKeyboardButton(text="Раздел запчастей", callback_data="parts"))
    keyboard.add(*btns)

    bot.send_message(message.chat.id, utils.help_text, parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def send_start(message): 
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    btns.append(types.InlineKeyboardButton(text="Помощь - help", callback_data="help"))
    keyboard.add(*btns)

    bot.send_message(message.chat.id, utils.start_text, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(commands=["time","t","ti","tim"])
def send_time(message): 
    bot.send_message(message.chat.id, utils.free_time, parse_mode='Markdown', reply_markup=time_keyboard(utils.time))

# функция получения статуса готовности авто
@bot.message_handler(commands=["status","s","stat"])
def send_status(message): 
    bot.statusFL = True
    bot.send_message(message.chat.id, "Введите гос.номер Вашего авто(А111АА196):")
    
    
# функция логина мастерак
@bot.message_handler(commands=["login"])
def login_func(message): 
    bot.send_message(message.chat.id, "Введите кодовое слово:")
    bot.loginFL = True

# функция выхода
@bot.message_handler(commands=["x","up"])
def exit_func(message): 
    bot.loginFL = False
    bot.statusFL = False
    bot.partsFL = False
    send_help(message)

#фцнкция перехода в раздел запчатсей
@bot.message_handler(commands=["parts"])
def parts_func(message): 
    bot.loginFL = False
    bot.statusFL = False
    bot.partsFL = True
    bot.send_message(message.chat.id, "Введите слово или фразу для поиска:")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    btns.append(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    keyboard.add(*btns)
    
    if bot.loginFL == True:
         if message.text == utils.code_word:
                bot.currentMaster_id = message.chat.id
                bot.send_message(message.chat.id, "Авторизован успешно")
    if bot.statusFL == True:
         bot.send_message(message.chat.id, "Статус автомобиля с номером: "+message.text+"\nГотов\nВведите /x чтобы вернуться назад", parse_mode='Markdown', reply_markup=keyboard)	
    if bot.partsFL == True:
         bot.send_message(message.chat.id, "По запросу: "+message.text+"\nничего не найдено\nВведите /x чтобы вернуться назад", parse_mode='Markdown', reply_markup=keyboard)		
    if (bot.loginFL == False and bot.statusFL == False and bot.partsFL == False):
         bot.send_message(message.chat.id, "Отправьте команду /help для получения справки")

def time_keyboard(time):
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    for x in time:
        btns.append(types.InlineKeyboardButton(text=(x.h+":"+x.m), callback_data=(x.h+":"+x.m)))
    keyboard.add(*btns)
    return keyboard

@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    """обработчик нажатия инлайн кнопок"""

    print(c.data)
    for x in utils.time:
        if c.data in x.data:
            bot.send_message(c.message.chat.id, "Забронировано успешно")
    if c.data == "help":
        send_help(c.message)
    if c.data == "time":
        send_time(c.message)
    if c.data == "status":
        send_status(c.message)
    if c.data == "parts":
        parts_func(c.message)
    if c.data == "back":
        exit_func(c.message)
        



if __name__ == '__main__':
    bot.polling(none_stop=True)
