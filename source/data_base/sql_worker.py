import sqlite3 as sql
import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from services import yaml_worker

def __get_final_time(time_inetral_name):
    time_interval = yaml_worker.get_time_interval(time_inetral_name)
    return (datetime.datetime.now() + time_interval)


def sql_start():
    global data_base
    global cursor 

    data_base = sql.connect("chocolate_bot.db")
    cursor = data_base.cursor()
    
    if data_base:
        print("[INFO] Data base is connect")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors(id INTEGER PRIMARY KEY AUTOINCREMENT, id_user TEXT, location TEXT, time_start TEXT, time_finish TEXT)")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors_waiting(id INTEGER PRIMARY KEY AUTOINCREMENT, id_user TEXT, location TEXT, time_start TEXT, time_finish TEXT, code INTEGER)")
    data_base.execute("CREATE TABLE IF NOT EXISTS visitors_stat(id_user PRIMARY KEY)")
    data_base.commit()

def get_waiting_keyboard():
    time_waiting = __get_final_time("waiting_time_interval").strftime('%H:%M:%S')

    keyboard = InlineKeyboardMarkup()

    query_1 = f'''
    SELECT id_user, MAX(id)
    FROM visitors_waiting
    WHERE time_finish < '{time_waiting}'
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

            button_add = InlineKeyboardButton("Принять", callback_data = str(user_data[1]) + "," + str(user_data[2]) + "," + "Принять")
            button_code = InlineKeyboardButton(user_data[5], callback_data = "Код")
            button_location = InlineKeyboardButton(user_data[2], callback_data= "Локация")

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

async def is_Trusted(id_user):
    trusted_time_interval = yaml_worker.get_time_interval("trusted_time_interval")
    time_interval = yaml_worker.get_time_interval("time_interval")
    trusted_time = (datetime.datetime.now() + time_interval) + trusted_time_interval

    cursor.execute(f"SELECT * FROM visitors WHERE id_user == '{id_user}' AND time_finish > '{trusted_time.strftime('%H:%M:%S')}' ORDER BY id DESC LIMIT 1;")
    request = cursor.fetchone()

    if request == None:
        return False
    else:
        return True

async def insert_visitor(id_user, location, db_name, time_interval_name, code = None):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    final_time = __get_final_time(time_interval_name).strftime("%H:%M:%S")
    if code == None:
        data_base.execute(f"""INSERT INTO {db_name} (id_user, location, time_start, time_finish) VALUES ('{id_user}', '{location}', '{current_time}', '{final_time}');""")
    else:
        data_base.execute(f"""INSERT INTO {db_name} (id_user, location, time_start, time_finish, code) VALUES ('{id_user}', '{location}', '{current_time}', '{final_time}', '{code}');""")
    data_base.commit()
    
    
async def is_final():
    current_time_dt = datetime.datetime.now().strftime("%H:%M:%S")
    cursor.execute(f"SELECT * FROM visitors WHERE time_finish > '{current_time_dt}' ORDER BY id DESC LIMIT 1;")
    request = cursor.fetchone()

    if request != None:
        current_time = datetime.datetime.now()
        time_finish = datetime.datetime.strptime(request[4], "%H:%M:%S")

        period = time_finish - current_time

        hours = period.seconds // 3600
        minutes = (period.seconds % 3600) // 60
        seconds = period.seconds % 60

        return f"Часов: {hours} Минут: {minutes} Секунд: {seconds}"
    else:
        return False

async def get_amount_visitors(button_name):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    cursor.execute(f"""SELECT count(*) FROM visitors WHERE location = '{yaml_worker.get_location(button_name)}' AND time_finish > '{current_time}';""")
    return "".join(map(str, cursor.fetchone()))

async def get_last_location(id_user):
    cursor.execute(f"SELECT * FROM visitors WHERE id_user == '{id_user}' ORDER BY id DESC LIMIT 1;")
    return str(cursor.fetchone()[2])

def sql_close():
    data_base.close()