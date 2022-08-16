from aiogram import types
from dispatcher import dp
from main import BotDB


# отклик на команду /start
@dp.message_handler(commands="start")
async def start(message: types.Message):

    print("fjkladg")

    # Проверка пользователя в базе данных по сообщению пользователя и в таком случае, добавление пользователя в БД
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id,str(message.from_user.full_name),str(message.from_user.username))

    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    school_subjects = types.KeyboardButton("🎒 Школьные предметы")
    professional_skills = types.KeyboardButton("Профессиональные навыки")
    markup.add(school_subjects, professional_skills)

    await message.bot.send_message(message.from_user.id, f"Привет <b>{message.from_user.first_name}!</b> Что хочешь изучить? <b>Школьные предметы</b>, или <b>профессиональные навыки</b>?", parse_mode='html', reply_markup=markup)

# все сообщения в чат
@dp.message_handler()
async def skills(message: types.Message):

    if not BotDB.get_know_skill_user(message.from_user.id) == BotDB.get_title_school_skills() or BotDB.get_title_profi_skills():
        BotDB.update_null_know_skill_user(message.from_user.id)

    if not BotDB.get_wknow_skill_user(message.from_user.id) == BotDB.get_title_school_skills() or BotDB.get_title_profi_skills():
        BotDB.update_null_wknow_skill_user(message.from_user.id)

    if message.text == "🎒 Школьные предметы":

        # Клавиатура
        markup = types.InlineKeyboardMarkup(row_width=2)

        # Цикл для клавиатуры
        for x in range(BotDB.get_count_school_skills()):
            markup = markup.add(types.InlineKeyboardButton(str(BotDB.get_title_school_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""), callback_data=str(BotDB.get_title_school_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",","")))

        await message.bot.send_message(message.from_user.id, "Здорово! Выбери предмет, в котором ты разбираешься!", reply_markup=markup)

    if message.text == "Профессиональные навыки":

        # Клавиатура
        markup = types.InlineKeyboardMarkup(row_width=2)

        # Цикл для клавиатуры
        for x in range(BotDB.get_count_profi_skills()):
            markup = markup.add(types.InlineKeyboardButton(str(BotDB.get_title_profi_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""), callback_data=str(BotDB.get_title_profi_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",","")))

        await message.bot.send_message(message.from_user.id, "Здорово! Выбери предмет, в котором ты разбираешься!", reply_markup=markup)

    # Цикл для навыков которые пользователь хочет подтянуть
    for x in range(BotDB.get_count_school_skills()):

        # Проверка чата на наличие названий школьных предметов
        if message.text == str(BotDB.get_title_school_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""):

            # Проверка на различие навыка который знает пользователь и который он хочет потдянуть
            if not message.text == str(BotDB.get_know_skill_user(message.from_user.id)[0]).replace("'","",2).replace("(","").replace(")","").replace(",",""):

                # Добавление в БД
                BotDB.add_user_wknow_skill(str(BotDB.get_title_school_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""), message.from_user.id)

            else:

                await message.bot.send_message(message.from_user.id, "Пожалуйста, выберите навык для изучения, отличающийся от навыка который вы знаете! Повторите попытку заново /start")
                break

            # Сообщения...
            await message.bot.send_message(message.from_user.id, "Круто! Мы подобрали для тебя <b>лучших людей</b> в своей сфере, можешь написать им!", reply_markup=None, parse_mode="html")
            await message.bot.send_message(message.from_user.id, "<b>Поиск...</b>", parse_mode="html")

            # Добавление данных о скилах пользователя из базы данных в локальную переменную
            user = BotDB.get_skills_user(message.from_user.id)[0]

            # Проверка на наличие подходяшего человека в базе данных(то есть, человек, который знает навык нужный пользователю и который хочет получить навык, который знает пользователь)
            if BotDB.get_need_user(user[1], user[0]):

                # Цикл для выявления всех подходящих пользователей и скидывание их в чат с пользователем
                for x in range(BotDB.get_count_need_user(user[1],user[0])):

                    #print(BotDB.get_need_user(user[1], user[0]))
                    await message.bot.send_message(message.from_user.id, str(x+1) + ". " + str(BotDB.get_need_user(user[1], user[0])[x]).replace("'","",4).replace("(","").replace(")","").replace(",",""))
            else:

                await message.bot.send_message(message.from_user.id, ":( К сожалению, таких пользователей не нашлось!")

            await message.bot.send_message(message.from_user.id, "Теперь если хочешь изменить свои предпочтения напиши команду <b>/start</b>", parse_mode="html")


    for x in range(BotDB.get_count_profi_skills()):

        # Проверка чата на наличие названий школьных предметов
        if message.text == str(BotDB.get_title_profi_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""):

            # Проверка на различие навыка который знает пользователь и который он хочет потдянуть
            if not message.text == str(BotDB.get_know_skill_user(message.from_user.id)[0]).replace("'","",2).replace("(","").replace(")","").replace(",",""):

                # Добавление в БД
                BotDB.add_user_wknow_skill(str(BotDB.get_title_profi_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""), message.from_user.id)
            else:

                await message.bot.send_message(message.from_user.id, "Пожалуйста, выберите навык для изучения, отличающийся от навыка который вы знаете! Повторите попытку заново /start")
                break

            # Сообщения...
            await message.bot.send_message(message.from_user.id, "Круто! Мы подобрали для тебя <b>лучших людей</b> в своей сфере, можешь написать им!", reply_markup=None, parse_mode="html")
            await message.bot.send_message(message.from_user.id, "<b>Поиск...</b>", parse_mode="html")

            # Добавление данных о скилах пользователя из базы данных в локальную переменную
            user = BotDB.get_skills_user(message.from_user.id)[0]

            # Проверка на наличие подходяшего человека в базе данных(то есть, человек, который знает навык нужный пользователю и который хочет получить навык, который знает пользователь)
            if BotDB.get_need_user(user[1], user[0]):

                # Цикл для выявления всех подходящих пользователей и скидывание их в чат с пользователем
                for x in range(BotDB.get_count_need_user(user[1],user[0])):

                    #print(BotDB.get_need_user(user[1], user[0]))
                    await message.bot.send_message(message.from_user.id, str(x+1) + ". " + str(BotDB.get_need_user(user[1], user[0])[x]).replace("'","",4).replace("(","").replace(")","").replace(",",""))
            else:

                await message.bot.send_message(message.from_user.id, ":( К сожалению, таких пользователей не нашлось!")

            await message.bot.send_message(message.from_user.id, "Теперь если хочешь изменить свои предпочтения напиши команду    <b>/start</b>", parse_mode="html")

# callback функция для Inline кнопок и для цикла следующей клавиатуры - ReplyButtons
@dp.callback_query_handler()
async def process_callback_button1(call: types.CallbackQuery):

    # callback штуки
    callback = call.data

    # Добавление в БД
    BotDB.add_user_know_skill(callback, call.from_user.id)

    # Удаление кнопок
    await call.message.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Цикл для следующей клавиатуры
    for x in range(BotDB.get_count_school_skills()):

        if callback == str(BotDB.get_title_school_skills()[x]).replace("'", "", 2).replace("(", "").replace(")","").replace(",", ""):

            for x in range(BotDB.get_count_school_skills()):
                x = types.KeyboardButton(str(BotDB.get_title_school_skills()[x]).replace("'","",2).replace("(","").replace(")","").replace(",",""))
                markup.insert(x)

    # Цикл для следующей клавиатуры
    for x in range(BotDB.get_count_profi_skills()):

        if callback == str(BotDB.get_title_profi_skills()[x]).replace("'", "", 2).replace("(", "").replace(")","").replace(",", ""):

            for x in range(BotDB.get_count_profi_skills()):
                x = types.KeyboardButton(str(BotDB.get_title_profi_skills()[x]).replace("'", "", 2).replace("(", "").replace(")","").replace(",", ""))
                markup.insert(x)

    # markup.add(str(BotDB.get_title_school_skills()[0]),str(BotDB.get_title_school_skills()[1]),str(BotDB.get_title_school_skills()[2]),str(BotDB.get_title_school_skills()[3]),str(BotDB.get_title_school_skills()[-1]))

    await call.message.bot.send_message(call.message.chat.id, "Спасибо! А теперь выбери предмет, который хочешь подтянуть", reply_markup=markup)




"""# отклик на команду /restart
@dp.message_handler(commands="restart")
async def start(message: types.Message):

    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    school_subjects = types.KeyboardButton("🎒 Школьные предметы")
    professional_skills = types.KeyboardButton("Профессиональные навыки")
    markup.add(school_subjects, professional_skills)

    await message.bot.send_message.

    await message.bot.send_message(message.from_user.id, f"Привет <b>{message.from_user.first_name}!</b> Что хочешь изучить? <b>Школьные предметы</b>, или <b>профессиональные навыки</b>?", parse_mode='html', reply_markup=markup)
"""