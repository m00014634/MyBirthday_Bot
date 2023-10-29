import sqlite3
from datetime import datetime
connection = sqlite3.connect('bot.db')
sql = connection.cursor()


# user table
sql.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT,date_of_birth TEXT,reg_date DATETIME);')

connection.commit()



def register_user(user_id,username=None,date_of_birth = None):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users VALUES (?,?,?,?);',(user_id,username,date_of_birth,datetime.now()))
    connection.commit()


def checker(user_id):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT user_id FROM users WHERE user_id=?;',(user_id,)).fetchone()

    if checker is None:
        return False
    else:
        return True


def user_info(user_id):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    user_info = sql.execute('SELECT * FROM users where user_id=?;',(user_id,)).fetchone()
    return user_info



def user_information():
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    user_info = sql.execute('SELECT * FROM users ;').fetchall()
    return user_info


def delete_user(user_id):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    sql.execute('DELETE  FROM users WHERE user_id=?;',(user_id,)).fetchall()

    connection.commit()


