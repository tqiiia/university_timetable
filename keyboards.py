from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

#   start keyboard
kb = InlineKeyboardMarkup(row_width=7,
                          resize_keyboard=True,
                          one_time_keyboard=True)
kb.add(InlineKeyboardButton('Расписание',           callback_data='group'),
       InlineKeyboardButton('Мероприятия недели',   callback_data='event'))

kb.add(InlineKeyboardButton('Обратная связь',       callback_data='feedback'),
       InlineKeyboardButton('Настройки',            callback_data='settings'))

#   schedule
kb_schedule = InlineKeyboardMarkup(row_width=7,
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
kb_schedule.add(InlineKeyboardButton('Эта неделя',          callback_data='schedule_this_week'),
                InlineKeyboardButton('Следующая неделя',    callback_data='schedule_next_week'))
kb_schedule.add(InlineKeyboardButton('Сегодня',             callback_data='schedule_this_day'),
                InlineKeyboardButton('Завтра',              callback_data='schedule_next_day'))

#   events
kb_events = InlineKeyboardMarkup(row_width=7,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
kb_events.add(InlineKeyboardButton('Волонтёрский корпус',       url='https://vk.com/volunteer_spbgau'))
kb_events.add(InlineKeyboardButton('Студ совет',                url='https://vk.com/spbgausc'),
              InlineKeyboardButton('Профком',                   url='https://vk.com/profkom_gau'))
kb_events.add(InlineKeyboardButton('Отряды',                    callback_data='squads'),
              InlineKeyboardButton('Спорт',                     callback_data='sport'))
kb_events.add(InlineKeyboardButton('Назад',                     callback_data='back'))

#   feedback
kb_feedback = InlineKeyboardMarkup(row_width=7,
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
kb_feedback.add(InlineKeyboardButton('Поддержка бота',                          callback_data='feedback_to_admin'))
kb_feedback.add(InlineKeyboardButton('Обратная связь по работе университета',   callback_data='feedback_to_university'))
kb_feedback.add(InlineKeyboardButton('Инструкция',                              callback_data='manual'),
                InlineKeyboardButton('Назад',                                   callback_data='back'))

#   settings
kb_settings = InlineKeyboardMarkup(row_width=7,
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
kb_settings.add(InlineKeyboardButton('Оповещения о занятиях на день',   callback_data='alerts_day'))
kb_settings.add(InlineKeyboardButton('Оповещение о начале занятий',     callback_data='alerts'))
kb_settings.add(InlineKeyboardButton('Назад',                           callback_data='back'))


kb_settings_1 = InlineKeyboardMarkup(row_width=7,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)
kb_settings_1.add(InlineKeyboardButton('Подтвердить',   callback_data='accept_1'),
                  InlineKeyboardButton('Отказаться',    callback_data='back'))


kb_settings_2 = InlineKeyboardMarkup(row_width=7,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)
kb_settings_2.add(InlineKeyboardButton('За 5 минут',    callback_data='5min'),
                  InlineKeyboardButton('За 10 минут',   callback_data='10min'),
                  InlineKeyboardButton('За 15 минут',   callback_data='15min'))
kb_settings_2.add(InlineKeyboardButton('Назад',         callback_data='back'))


kb_settings_3 = InlineKeyboardMarkup(row_width=7,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)
kb_settings_3.add(InlineKeyboardButton('Подтвердить',   callback_data='accept_3'),
                  InlineKeyboardButton('Отказаться',    callback_data='back'))

#   groups_list
btn_list_groups = []
with open('groups.txt', 'r') as g:
    for group in g:
        btn_list_groups.append(group.split()[0].replace('0', 'О').replace('O', 'О').replace('B', 'В'))
btn_list_groups.sort()

kb_groups = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True)


async def user_group_kb(user_group):
    kb_groups.clean()
    if user_group:
        kb_groups.add(f'{user_group}')
    for btn in btn_list_groups:
        kb_groups.add(btn)


#   back kb
kb_back = InlineKeyboardMarkup(row_width=7,
                               resize_keyboard=True,
                               one_time_keyboard=True)
kb_back.add(InlineKeyboardButton('Назад',   callback_data='back'))
