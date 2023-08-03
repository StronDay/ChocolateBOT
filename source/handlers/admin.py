from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot
from keyboards import keyboard_admin_default, keyboard_admin_admin, get_buttons, get_all_button_info_inline, get_buttons_pallet, malling_keyboard, ad_moderator_keyboard
from keyboards import cd_button_action, cd_button_add
from services import yaml_worker
from filters import button_filter
from data_base import sql_worker

class FSMAdmin(StatesGroup):
    name = State()
    new_name = State()
    location = State()

class FSMMalling(StatesGroup):
    message = State()

class FSMAdminAdd(StatesGroup):
    name = State()
    location = State()
    simple = State()

class FSMAdminLocation(StatesGroup):
    name = State()
    new_name = State()
    location = State()

#commands = "/Панель_администратора"
async def command_admin_panel(message : types.Message):
    await bot.send_message(message.from_user.id, "Чего изволите сегодня?", reply_markup = keyboard_admin_admin)

#commands = "/Панель_модератора"
async def command_moder_panel(message : types.Message):
    await bot.send_message(message.from_user.id, "Вы в режиме вашего работника", reply_markup = ad_moderator_keyboard)

#commands = "/Обычная_панель"
async def command_default_panel(message : types.Message):
    await bot.send_message(message.from_user.id, "Вы вернулись в режим простолюдиинов", reply_markup = keyboard_admin_default())

#commands = "/Инфа_все_кнопки"
async def command_all_info_button(message : types.Message):
    await bot.send_message(message.from_user.id, "Вот полная инофрмация о названиях кнопок и их локации", reply_markup = get_all_button_info_inline("info"))

#Панель рассылки
async def command_mailing_settings(message : types.Message):
    await bot.send_message(message.from_user.id, "Что планируете сделать?", reply_markup = malling_keyboard)

#Обновление пользователей для рассылки
async def command_save_into_sql(message : types.Message):
    await sql_worker.refresh_visitors_stat()
    await bot.send_message(message.from_user.id, "Список пользователей в бд обновлён")

#Рассылка 1
async def command_start_malling(message : types.Message):
    await FSMMalling.message.set()
    await bot.send_message(message.from_user.id, "Введите сообщение для рассылки:")

#Рассылка 2 final
async def command_start_malling_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["message"] = message.text

    visitors = await sql_worker.get_all_state_visitors_id()
    for visitor in visitors:
        await bot.send_message(visitor[0], data["message"])

    await bot.send_message(message.from_user.id, "Рассылка выполнена")
    await state.finish()
    
#commands = "/Изменить_название" 1 start
async def command_button_name_change(message : types.Message):
    await FSMAdmin.name.set()
    await bot.send_message(message.from_user.id, "Название какой кнопки вы хотите изменить?", reply_markup = get_buttons("change"))

#commands = "/Изменить_название" 2
async def choice_button_change(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    async with state.proxy() as data:
        data["name"] = callback_data.get("button")

    await FSMAdmin.next()
    await bot.send_message(call.from_user.id, "Напишите нове название кнопки:")

#commands = "/Изменить_название" 3 finish
async def choice_new_button_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["new_name"] = message.text

    async with state.proxy() as data:
        yaml_worker.change_hobby_button(data["name"], data["new_name"], find_mode=yaml_worker.FindMode.NAME)

    await bot.send_message(message.from_user.id, "Название кнопки было успешно изменено")
    await state.finish()

#commands = "/Изменить_локацию" 1 start
async def command_button_location_change(message : types.Message):
    await FSMAdminLocation.name.set()
    await bot.send_message(message.from_user.id, "Название локации для какой кнопки вы хотите изменить?", reply_markup = get_buttons("change_location"))

#commands = "/Изменить_локацию" 2
async def choice_button_location_change(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    async with state.proxy() as data:
        data["name"] = callback_data.get("button")

    await FSMAdminLocation.next()
    await bot.send_message(call.from_user.id, f"Напишите нове название локации для кнопки '{data['name']}':")

#commands = "/Изменить_локацию" 3 finish
async def choice_new_button_location(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["new_name"] = message.text

    async with state.proxy() as data:
        yaml_worker.change_hobby_button(data["name"], data["new_name"], find_mode=yaml_worker.FindMode.LOCATIONS)

    await bot.send_message(message.from_user.id, f"Название локации для кнопки '{data['name']}' было успешно изменено")
    await state.finish()

#commands = "/Удалить_кнопку" 1 start
async def command_button_delete(message : types.Message):
    await FSMAdmin.name.set()
    await bot.send_message(message.from_user.id, "Какую кнопку вы хотите удалить?", reply_markup = get_buttons("delete"))

#commands = "/Удалить_кнопку" 2 final
async def choice_button_delete(call : types.CallbackQuery, callback_data: dict,  state : FSMContext):
    yaml_worker.delete_hobby_button(callback_data.get("button"))

    await bot.send_message(call.from_user.id, "Кнопка была удалена")
    await state.finish()

#commands = "/Добавить_кнопку" 1 start
async def command_button_add(message : types.Message):
    await FSMAdminAdd.name.set()
    await bot.send_message(message.from_user.id, "Дайте название новой кнопки:")

#commands = "/Добавить_кнопку" 2
async def choise_name_button_add(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await FSMAdminAdd.next()
    await bot.send_message(message.from_user.id, "Дайте название локации для новой кнопки:")

#commands = "/Добавить_кнопку" 3
async def choise_location_button_add(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["location"] = message.text

    await FSMAdminAdd.next()
    await bot.send_message(message.from_user.id, "Выберете рассположение для новой кнопки:", reply_markup=get_buttons_pallet("add"))

#commands = "/Добавить_кнопку" 4 finish
async def button_add(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    async with state.proxy() as data:
        yaml_worker.add_hobby_button({"name": data["name"], "location": data["location"]}, callback_data.get("i"), callback_data.get("j"))

    await bot.send_message(call.from_user.id, "Кнопка успешно добавлена")
    await state.finish()

#commands = "/Отменить"
async def cancel_state(call : types.CallbackQuery, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await bot.send_message(call.from_user.id, "Вы отменили процесс")
    await state.finish()

async def info_button(call : types.CallbackQuery, callback_data: dict):
    await bot.send_message(call.from_user.id, f"{callback_data.get('button')}")

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(info_button, button_filter.isAdmin(), cd_button_action.filter(action = "info"))

    dp.register_message_handler(command_admin_panel, button_filter.isAdmin(), commands = "Панель_администратора")
    dp.register_message_handler(command_moder_panel, button_filter.isAdmin(), commands = "Панель_модератора")
    dp.register_message_handler(command_default_panel, button_filter.isAdmin(), commands = "Обычная_панель")
    dp.register_message_handler(command_all_info_button, button_filter.isAdmin(), commands = "Инфа_все_кнопки")
    dp.register_message_handler(command_mailing_settings, button_filter.isAdmin(), commands = "Управление_рассылкой")
    dp.register_message_handler(command_save_into_sql, button_filter.isAdmin(), commands = "Записать_новых_пользователей_в_бд")

    dp.register_message_handler(command_start_malling, button_filter.isAdmin(), commands = "Сделать_рассылку", state=None)
    dp.register_message_handler(command_start_malling_message, button_filter.isAdmin(), state=FSMMalling.message)

    dp.register_message_handler(command_button_delete, button_filter.isAdmin(), commands = "Удалить_кнопку", state=None)
    dp.register_callback_query_handler(choice_button_delete, button_filter.isAdmin(), cd_button_action.filter(action = "delete"), state=FSMAdmin.name)

    dp.register_message_handler(command_button_add, button_filter.isAdmin(), commands = "Добавить_кнопку", state=None)
    dp.register_message_handler(choise_name_button_add, button_filter.isAdmin(), state=FSMAdminAdd.name)
    dp.register_message_handler(choise_location_button_add, button_filter.isAdmin(), state=FSMAdminAdd.location)
    dp.register_callback_query_handler(button_add, button_filter.isAdmin(), cd_button_add.filter(action = "add"), state=FSMAdminAdd.simple)

    dp.register_message_handler(command_button_name_change, button_filter.isAdmin(), commands = "Изменить_название", state=None)
    dp.register_callback_query_handler(choice_button_change, button_filter.isAdmin(), cd_button_action.filter(action = "change"), state = FSMAdmin.name)
    dp.register_message_handler(choice_new_button_name, button_filter.isAdmin(), state=FSMAdmin.new_name)

    dp.register_message_handler(command_button_location_change, button_filter.isAdmin(), commands = "Изменить_локацию", state=None)
    dp.register_callback_query_handler(choice_button_location_change, button_filter.isAdmin(), cd_button_action.filter(action = "change_location"), state = FSMAdminLocation.name)
    dp.register_message_handler(choice_new_button_location, button_filter.isAdmin(), state=FSMAdminLocation.new_name)

    dp.register_callback_query_handler(cancel_state, button_filter.isModer(), Text(equals="Отменить"), state="*")