import datetime
import os 

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from keyboards import cd_button_action, cd_button_add
from yaml import full_load
from yaml import safe_dump
from enum import Enum

class FindMode(Enum):
    NAME = 1
    LOCATIONS = 2

current_directory = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()

path_to_buttons_cfg = "../buttons_cfg.yaml"
absolute_path_to_buttons_cfg = os.path.join(current_dir, path_to_buttons_cfg)

puth_to_text = "text.yaml"
absolute_path_to_text = os.path.join(current_dir, puth_to_text)

path_to_time_interval = "time_interval.yaml"
absolute_path_to_time_interval = os.path.join(current_dir, path_to_time_interval)



def yaml_full_load(path_to_yaml = absolute_path_to_buttons_cfg):
    with open(path_to_yaml, 'r') as file:
        data = full_load(file)

    return data

def yaml_push(data):
    with open(absolute_path_to_buttons_cfg, 'w', encoding = "utf-8") as file:
        safe_dump(data, file, allow_unicode=True) 

def get_hobby_buttons_replay():
    data = yaml_full_load()

    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)

    arr = []
    for row in data["hobby_button"]:
        for button in row: 
            arr.append(KeyboardButton(button["name"]))
        reply_keyboard.row(*arr)
        arr.clear()

    return reply_keyboard

def get_hobby_location_inline(action: str):
    data = yaml_full_load()

    inline_keyboard = InlineKeyboardMarkup()

    for row in data["hobby_button"]:
        for button in row: 
            inline_keyboard.row(InlineKeyboardButton(button["name"], callback_data = cd_button_action.new(button = button["name"], action = action)),
                                InlineKeyboardButton(button["location"], callback_data = cd_button_action.new(button = button["location"], action = action)))

    return inline_keyboard

def get_hobby_buttons_pallet(action):

    data = yaml_full_load()

    inline_keyboard = InlineKeyboardMarkup()
    button_new_row = InlineKeyboardButton("+", callback_data = cd_button_add.new(button = "new", i = "new", j = "new", action = action))

    arr = []
    for i, row in enumerate(data["hobby_button"]):
        for j, button in enumerate(row):
            arr.append(InlineKeyboardButton("+", callback_data = cd_button_add.new(button = button["name"], i = str(i), j = str(j), action = action)))
            arr.append(InlineKeyboardButton(button["name"], callback_data = cd_button_add.new(button = button["name"], j = "none", i = "none", action = "none")))
        arr.append(InlineKeyboardButton("+", callback_data = cd_button_add.new(button = button["name"], i = str(i), j = str(j + 1), action = action)))
        inline_keyboard.row(*arr)
        arr.clear()

    inline_keyboard.row(button_new_row)
    return inline_keyboard

def get_hobby_buttons_inline(action: str):
    data = yaml_full_load()

    inline_keyboard = InlineKeyboardMarkup(resize_keyboard = True)

    for row in data["hobby_button"]:
        for button in row: 
            inline_keyboard.add(InlineKeyboardButton(button["name"], callback_data = cd_button_action.new(button = button["name"], action = action)))

    return inline_keyboard

def is_hobby_button(target: str, find_mode: FindMode = None) -> bool:
    if find_hobby_button(target, find_mode) == None:
        return False
    else:
        return True
            
def find_hobby_button(target: str, find_mode: FindMode):
    data = yaml_full_load()

    for row in data["hobby_button"]:
        for button in row:
            if find_mode == FindMode.LOCATIONS:
                if button["location"] == target:
                    return button
            else:
                if button["name"] == target:
                    return button
                
def delete_hobby_button(del_button: dict):
    data = yaml_full_load()

    for i, row in enumerate(data["hobby_button"]):
        for j, button in enumerate(row):
            if button["location"] == del_button["location"] and button["name"] == del_button["name"]:
                del data["hobby_button"][i][j]
                break

    data["hobby_button"] = [row for row in data["hobby_button"] if row and row != []]

    yaml_push(data)

def delete_hobby_button(name: str):
    data = yaml_full_load()

    for i, row in enumerate(data["hobby_button"]):
        for j, button in enumerate(row):
            if button["name"] == name:
                del data["hobby_button"][i][j]
                break

    data["hobby_button"] = [row for row in data["hobby_button"] if row and row != []]

    yaml_push(data)

def change_hobby_button(cur_button: dict, new_button: dict):
    data = yaml_full_load()

    for i, row in enumerate(data["hobby_button"]):
        for j, button in enumerate(row):
            if button["location"] == cur_button["location"] and button["name"] == cur_button["name"]:
                data["hobby_button"][i][j] = new_button
                break
    
    yaml_push(data)

def change_hobby_button(cur_element: str, new_element: str, find_mode: FindMode):
    data = yaml_full_load()

    if find_mode == FindMode.NAME:
        for i, row in enumerate(data["hobby_button"]):
            for j, button in enumerate(row):
                if button["name"] == cur_element:
                    data["hobby_button"][i][j]["name"] = new_element
                    break

    if find_mode == FindMode.LOCATIONS:
        for i, row in enumerate(data["hobby_button"]):
            for j, button in enumerate(row):
                if button["name"] == cur_element:
                    data["hobby_button"][i][j]["location"] = new_element
                    break
    
    yaml_push(data)

def add_hobby_button(new_button: dict, i, j):
    data = yaml_full_load()

    if i == "new" and j == "new" :
        data["hobby_button"].append([new_button])
    else:
        data["hobby_button"][int(i)].insert(int(j), new_button)

    yaml_push(data)

def get_hobby_button_reply():
    data = yaml_full_load()

    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)

    arr = []
    for row in data["hobby_button"]:
        for button in row: 
            arr.append(KeyboardButton(button["name"]))
        reply_keyboard.row(*arr)
        arr.clear()

    return reply_keyboard

def get_location(button_name):
    return find_hobby_button(button_name, FindMode.NAME)["location"]

def get_button_name(location):
    return find_hobby_button(location, FindMode.LOCATIONS)["name"]

def get_time_interval(name_var):
    data = yaml_full_load(absolute_path_to_time_interval)

    data_hours = data[name_var][0]["hours"]
    data_minutes = data[name_var][1]["minutes"]
    data_seconds = data[name_var][2]["seconds"]

    return datetime.timedelta(hours=data_hours, minutes=data_minutes, seconds=data_seconds)

def get_text(text_name):
    data = yaml_full_load(absolute_path_to_text)
    return data[text_name]
