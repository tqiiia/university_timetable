from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from auth_data import TOKEN_API
from messages import START_MESSAGE
from keyboards import kb, kb_groups, kb_feedback, kb_events, kb_settings, kb_settings_1, kb_settings_2, kb_settings_3, kb_back, kb_schedule, user_group_kb
from schedule import schedule_week, schedule_day
from data_base import db_start, create_profile, edit_profile

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


class reg(StatesGroup):
    group = State()
    alerts = State()
    end = State()


async def on_startup(_):
    await db_start()
    print('Бот успешно запущен')


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    user_group = await create_profile(user_id=message.from_user.id)
    await user_group_kb(user_group)
    await message.answer(START_MESSAGE, reply_markup=kb)
    await message.delete()


@dp.callback_query_handler(lambda c: c.data == 'group')
async def groups_list(callback_query: CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id,
                           text='Выберите группу:',
                           reply_markup=kb_groups)
    await reg.group.set()


@dp.callback_query_handler(lambda c: c.data == 'event')
async def events(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Ссылки на группы внеучебной деятельности университета:',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_events)


@dp.callback_query_handler(lambda c: c.data == 'feedback')
async def feedback(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Если возник какой-то вопрос, то можете оставлять свою обратную связь здесь:',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_feedback)


@dp.callback_query_handler(lambda c: c.data == 'settings')
async def settings(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Выберите режим оповещений:',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings)


@dp.callback_query_handler(lambda c: c.data == 'alerts_day')
async def alerts_day(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Подтвердите и вы будете получать оповещения о занятиях каждое утро',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings_1)


@dp.callback_query_handler(lambda c: c.data == 'alerts')
async def alerts(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Выберите за сколько вы хотите получать уведомления:',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings_2)


@dp.callback_query_handler(lambda c: c.data == '5min')
async def alerts_5min(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Подтвердите и вы будете получать оповещения о занятиях за 5 минут до их начала',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings_3)


@dp.callback_query_handler(lambda c: c.data == '10min')
async def alerts_10min(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Подтвердите и вы будете получать оповещения о занятиях за 10 минут до их начала',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings_3)


@dp.callback_query_handler(lambda c: c.data == '15min')
async def alerts_15min(callback_query: CallbackQuery):
    await bot.edit_message_text(text='Подтвердите и вы будете получать оповещения о занятиях за 15 минут до их начала',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb_settings_3)


@dp.message_handler(state=reg.group)
async def group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await edit_profile(state, user_id=message.from_user.id)
    await message.answer(text='Выберите режим отображения расписания:',
                         reply_markup=kb_schedule)
    await reg.end.set()


@dp.callback_query_handler(lambda c: c.data == 'schedule_this_week', state=reg.end)
async def schedule_this_week(callback_query: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Подгружаем расписание...')
    data = await state.get_data()
    await bot.send_message(callback_query.from_user.id,
                           text=f"{await schedule_week(str(data.get('group')), 0)}",
                           parse_mode='HTML',
                           reply_markup=kb_back)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'schedule_next_week', state=reg.end)
async def schedule_next_week(callback_query: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Подгружаем расписание...')
    data = await state.get_data()
    await bot.send_message(callback_query.from_user.id,
                           text=f"{await schedule_week(str(data.get('group')), 1)}",
                           parse_mode='HTML',
                           reply_markup=kb_back)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'schedule_this_day', state=reg.end)
async def schedule_this_day(callback_query: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Подгружаем расписание...')
    data = await state.get_data()
    await bot.send_message(callback_query.from_user.id,
                           text=f"{await schedule_day(str(data.get('group')))}",
                           parse_mode='HTML',
                           reply_markup=kb_back)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'schedule_next_day', state=reg.end)
async def schedule_next_day(callback_query: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Подгружаем расписание...')
    data = await state.get_data()
    await bot.send_message(callback_query.from_user.id,
                           text=f"{await schedule_day(str(data.get('group')), 1)}",
                           parse_mode='HTML',
                           reply_markup=kb_back)
    await state.finish()


#   Обработчик неверных команд
@dp.message_handler()
async def error(message: types.Message):
    await message.answer('Нет такой команды')


#   func back
@dp.callback_query_handler(lambda c: c.data == 'back')
async def back(callback_query: CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Вы вернулись назад')
    await bot.send_message(callback_query.from_user.id,
                           text=f'{START_MESSAGE}',
                           reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup)
