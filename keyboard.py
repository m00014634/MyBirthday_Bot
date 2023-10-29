from telebot import types

def admin():
    markup = types.ReplyKeyboardMarkup()
    kb_add = types.KeyboardButton('Добавить нового пользователя')
    kb_delete = types.KeyboardButton('Удалить пользователя')
    kb_all_users = types.KeyboardButton('Все пользователи')
    markup.add(kb_add,kb_delete,kb_all_users)
    return markup