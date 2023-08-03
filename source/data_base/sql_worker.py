import sqlite3 as sql
import datetime
from create_bot import bot

from datetime import timedelta
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from services import yaml_worker
from keyboards import training_choise_keyboard

from keyboards import moderator_keyboard

def __get_final_time(time_inetral_name):
    time_interval = yaml_worker.get_time_interval(time_inetral_name)
    return (datetime.datetime.now() + time_interval)

def __get_final_trust_time():
    final_time = yaml_worker.get_time_interval("time_interval")
    trust_time = yaml_worker.get_time_interval("trusted_time_interval")
    return (datetime.datetime.now() + final_time + trust_time)


def sql_start():
    global data_base
    global cursor 

    data_base = sql.connect("chocolate_bot.db")
    cursor = data_base.cursor()
    
    if data_base:
        print("[INFO] Data base is connect")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors(id INTEGER PRIMARY KEY AUTOINCREMENT, id_user TEXT, location TEXT, time_start TEXT, time_finish TEXT, time_trust TEXT)")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors_waiting(id INTEGER PRIMARY KEY AUTOINCREMENT, id_user TEXT, location TEXT, time_start TEXT, time_finish TEXT, code INTEGER)")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors_stat(id_user PRIMARY KEY)")
    data_base.commit()

#Получение из бд время окончания тренировки пользователя 
async def get_finish_time(user_id):
    pass

#Получение интервала времени из yaml файла
def get_time_interval(yaml_interval):
    pass

#Получение строки содержащей формат времени (Час|Минута|Секунда)
async def get_str_time(full_time):
    pass

def get_waiting_keyboard():
    current_time = datetime.datetime.now()

    keyboard = InlineKeyboardMarkup()

    query_1 = f'''
    SELECT id_user, MAX(id)
    FROM visitors_waiting
    WHERE time_finish > '{current_time}'
    GROUP BY id_user
    '''
    query_2 = '''
    SELECT * FROM visitors_waiting
    WHERE id_user = ? AND id = ?
    '''

    cursor.execute(query_1)
    result = cursor.fetchall()
    if result == None:
        return keyboard
    else:
        for row in result:
            id_user, max_id = row
            cursor.execute(query_2, (id_user, max_id))
            user_data = cursor.fetchone()

            button_add = InlineKeyboardButton("Принять", callback_data = moderator_keyboard.cd_accept.new(id_user = str(user_data[1]), location = str(user_data[2])))
            button_code = InlineKeyboardButton(user_data[5], callback_data = moderator_keyboard.cd_code.new(code = str(user_data[5])))
            button_location = InlineKeyboardButton(user_data[2], callback_data = moderator_keyboard.cd_location.new(location = str(user_data[2])))
            keyboard.row(button_add, button_code, button_location)
    return keyboard

async def refresh_visitors_stat():
    cursor.execute("INSERT OR IGNORE INTO visitors_stat SELECT DISTINCT id_user FROM visitors")
    data_base.commit()

async def get_all_state_visitors_id():
    cursor.execute("SELECT * FROM visitors_stat")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append(row)

    return data

async def insert_visitor(id_user, location):
    current_time = datetime.datetime.now()
    final_time = __get_final_time("time_interval")
    trust_time = __get_final_trust_time()

    query = f'''
    INSERT INTO visitors (id_user, location, time_start, time_finish, time_trust)
    VALUES ('{id_user}', '{location}', '{current_time}', '{final_time}', '{trust_time}');
    '''

    data_base.execute(query)
    data_base.commit()

async def insert_waiting(id_user, location, code):
    current_time = datetime.datetime.now()
    waiting_time = __get_final_time("waiting_time_interval")

    query = f'''
    INSERT INTO visitors_waiting (id_user, location, time_start, time_finish, code)
    VALUES ('{id_user}', '{location}', '{current_time}', '{waiting_time}', '{code}');
    '''

    data_base.execute(query)
    data_base.commit()

async def is_Trusted(id_user):
    current_time = datetime.datetime.now()

    cursor.execute(f"SELECT * FROM visitors WHERE id_user == '{id_user}' AND time_trust > '{current_time}' ORDER BY id DESC LIMIT 1;")
    request = cursor.fetchone()

    if request == None:
        return False
    else:
        return True
    
async def is_final():
    current_time = datetime.datetime.now()

    cursor.execute(f"SELECT * FROM visitors WHERE time_finish > '{current_time}' ORDER BY id DESC LIMIT 1;")
    request = cursor.fetchone()

    if request != None:
        current_time = datetime.datetime.now()
        time_finish = datetime.datetime.strptime(request[4], '%Y-%m-%d %H:%M:%S.%f')

        period = time_finish - current_time

        hours = period.seconds // 3600
        minutes = (period.seconds % 3600) // 60
        seconds = period.seconds % 60

        return f"Часов: {hours} | Минут: {minutes} | Секунд: {seconds}"
    else:
        return False

async def get_amount_visitors(button_name):
    current_time = datetime.datetime.now()
    cursor.execute(f"""SELECT count(*) FROM visitors WHERE location = '{yaml_worker.get_location(button_name)}' AND time_finish > '{current_time}';""")
    return "".join(map(str, cursor.fetchone()))

async def get_last_location(id_user):
    cursor.execute(f"SELECT * FROM visitors WHERE id_user == '{id_user}' ORDER BY id DESC LIMIT 1;")
    return str(cursor.fetchone()[2])

async def change_finish_time(id_user, new_time):
    trust_time = yaml_worker.get_time_interval("trusted_time_interval")
    new_time_trust = new_time + trust_time

    query = f'''
    UPDATE visitors
    SET time_finish = '{new_time}', time_trust = '{new_time_trust}'
    WHERE id = (
    SELECT MAX(id)
    FROM visitors
    WHERE id_user = '{id_user}'
    )
    '''

    data_base.execute(query)
    data_base.commit()

async def extend_time(id_user, extension):
    current_time = datetime.datetime.now()
    cursor.execute(f"SELECT * FROM visitors WHERE id_user == '{id_user}' AND time_trust > '{current_time}' ORDER BY id DESC LIMIT 1;")
   
    request = cursor.fetchone()
    new_time = datetime.datetime.strptime(request[4], "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=int(extension))
    await change_finish_time(id_user, new_time)

async def complete_time(id_user):
    time_complite = datetime.datetime.now()
    await change_finish_time(id_user, time_complite)

async def check_remaining_time():
    current_time = datetime.datetime.now()

    cursor.execute(f"SELECT id_user, time_finish FROM visitors WHERE time_finish > '{current_time}' AND time_finish - '{current_time}' <= 60")
    users = cursor.fetchall()

    if users != None:
        for user in users:
            user_id = user[0]

            period = datetime.datetime.strptime(user[1], '%Y-%m-%d %H:%M:%S.%f') - current_time
            hours = period.seconds // 3600
            minutes = (period.seconds % 3600) // 60
            seconds = period.seconds % 60

            await bot.send_message(user_id, f"До конца текущей тренировки осталось\nЧасов: {hours} | Минут: {minutes} | Секунд: {seconds}", reply_markup = training_choise_keyboard)


def sql_close():
    data_base.close()