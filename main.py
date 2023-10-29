from datetime import datetime
import telebot
import model
import keyboard as kb
from auth_data import TOKEN

bot = telebot.TeleBot(TOKEN)



"""START"""
@bot.message_handler(commands=['start'])
def start(message):
    check = model.checker(message.chat.id)
    if not check:
        bot.send_message(message.chat.id, 'Привет, отправьте дату своего рождения.\n'
                                           'Обязательно в формате Число-Месяц-Год.Например: 15-06-2001')
        bot.register_next_step_handler(message, register_user)
    else:
        all_users(message)


def register_user(message):

    try:
        birthday_info = message.text
        user_id = message.chat.i
        username = message.from_user.username
        d = datetime.strptime(birthday_info, "%d-%m-%Y")
        d = d.date()
        user_birthday = d.isoformat()
        model.register_user(user_id,username,user_birthday)
        bot.send_message(message.chat.id, 'Отлично,я запомнил вашу дату рождения!')
        all_users(message)

    except ValueError:
        bot.send_message(message.chat.id, 'Вы неправильно прописали дату,следуйте по такому формату:\n'
                                               'Число-Месяц-Год: Например: 15-06-2001\nНажмите на /start и начните заново. ')



def all_users(message):
    b = model.user_information()
    current_date = datetime.now().date().isoformat()
    for i in b:
        if current_date in i[2]:
            bot.send_message(message.chat.id,f'С днем рождения @{i[1]}!\nПусть этот день будет наполнен незабываемыми моментами!')




"""ADMIN"""
@bot.message_handler(commands=['admin'])
def admin_command(message):
    bot.send_message(message.chat.id,'Что вы хотите сделать?',reply_markup=kb.admin())
    bot.register_next_step_handler(message,admin)


"""ADMIN FUNCTIONS"""
def admin(message):
    bot.send_message(message.chat.id,'Отлично',reply_markup=telebot.types.ReplyKeyboardRemove())
    if message.text == 'Добавить нового пользователя':
        get_name(message)

    elif message.text == 'Удалить пользователя':
        which_user(message)

    elif message.text == 'Все пользователи':
       see_all_users(message)

def get_name(message):
    bot.send_message(message.chat.id,'Напишите имя пользователя')
    bot.register_next_step_handler(message,get_id)


def get_id(message):
    name = message.text
    bot.send_message(message.chat.id,'Дайте уникальное ID пользователю')
    bot.register_next_step_handler(message,get_date_of_birth,name)


def get_date_of_birth(message,name):
    id = message.text
    bot.send_message(message.chat.id,'Напишите дату рождения')
    bot.register_next_step_handler(message,admin_creates_user,name,id)


def admin_creates_user(message,name,id):
    username = name
    birthday = message.text
    user_id = id
    model.register_user(user_id,username,birthday)
    bot.send_message(message.chat.id,f'Новый пользователь успешно добавлен')


def which_user(message):
    user_id_info = [i[0] for i in model.user_information()]
    select_user_id = model.user_information()
    bot.send_message(message.chat.id,'Какого пользователя вы хотите удалить?')
    for i in select_user_id:
        bot.send_message(message.chat.id,f'{i[0]} - {i[1]}')
    bot.register_next_step_handler(message,delete_user,user_id_info)


def delete_user(message,user_id_info):
    try:
        user_id = int(message.text)
        if user_id in user_id_info:
            model.delete_user(user_id)
            bot.send_message(message.chat.id,'Пользователь успешно удален')
        else:
            bot.send_message(message.chat.id,'Такого пользователя нет')
    except ValueError:
        bot.send_message(message.chat.id,'Неправильно введен айди пользователя')
        which_user(message)


def see_all_users(message):
    users = [i for i in model.user_information()]
    for i in users:
        bot.send_message(message.chat.id,f'{i[0],i[1]}')


"""TEXT"""
@bot.message_handler(content_types=['text'])
def text_obrabotchik(message):
    bot.send_message(message.chat.id,'Эмм,что-то пошло не так...')






bot.polling()
