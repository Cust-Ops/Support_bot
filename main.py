import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import botkeyboards as kb  # Keyboard with answers for users
import jiraintegration as ji  # All for integration with jira software
import config  # All confidential properties
import HBotBD  # Работа бота с БД PostgreSQL

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.token_bot_main, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserAnswers(StatesGroup):
    waiting_for_user_answer_y = State()
    waiting_for_user_answer_n = State()
    waiting_for_user_issue = State()
    waiting_for_user_picture = State()
    waiting_for_issue_number = State()


# First message for users
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    HBotBD.create_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                           message.from_user.last_name)
    await message.answer('Добро пожаловать в бота технической поддержки. Для начала работы, '
                         'выберите кнопку "создание запроса" или "Статус запроса" на клавиатуре бота. '
                         'Если вы не видите клавиатуру бота, нажмите иконку в виде плитки, она '
                         'находится в текстовом поле справа.', reply_markup=kb.ReplyKeyboardRemove())
    await message.answer('<a href="https://clck.ru/WTy9V">Обучающий материал по использованию бота</a>',
                         reply_markup=kb.requests_kb)


@dp.message_handler(content_types=['text'])
async def bitrix_help(message: types.Message):
    if message.text.lower() == "создание запроса":
        HBotBD.create_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                               message.from_user.last_name)
        print(f'Пришел запрос на создание заявки от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        await message.bot.send_message(config.chat_id, f'Поступил запрос помощи от '
                                       f'{message.from_user.first_name} {message.from_user.last_name}, '
                                       f'ожидайте последующего сообщения с информацией')
        await message.answer('Вы хотите приложить скриншот или документ к запросу?', reply_markup=kb.inline_yn_full)
    elif message.text.lower() == "статус запроса":
        HBotBD.create_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                               message.from_user.last_name)
        print(f'Запрос статуса задачи от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        await message.answer('Отправьте номер вашей заявки.')
        await UserAnswers.waiting_for_issue_number.set()
    else:
        HBotBD.create_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                               message.from_user.last_name)
        await message.answer('Вы совершили ошибку при использовании бота.', reply_markup=kb.requests_kb)
        await message.bot.send_photo(message.from_user.id, photo=open('/opt/Python_bot/Support_bot/errorpicd.png', 'rb'),
                                     reply_markup=kb.requests_kb)


@dp.callback_query_handler(lambda c: c.data == 'btn_y')
async def picture_y(message: types.Message):
    logging.info('К запросу приложен документ')
    config.docav = True
    await message.bot.send_message(message.from_user.id, 'Отправьте желаемый файл')
    await UserAnswers.waiting_for_user_picture.set()


@dp.callback_query_handler(lambda c: c.data == 'btn_n')
async def picture_n(message: types.Message):
    config.docav = False
    await message.bot.send_message(message.from_user.id, 'Опишите вашу проблему. '
                                   'Помните,что ваш запрос должен быть оформлен в одном сообщении.')
    await UserAnswers.waiting_for_user_issue.set()


@dp.message_handler(state=UserAnswers.waiting_for_user_picture, content_types=['document', 'text'])
async def take_a_picture(message: types.Message):
    await message.answer('Документ приложен. Теперь опишите свою проблему. Помните, '
                         'что ваш запрос должен быть оформлен в одно сообщение.')
    await message.bot.forward_message(config.chat_id, message.chat.id, message.message_id)
    await UserAnswers.waiting_for_user_issue.set()


@dp.message_handler(state=UserAnswers.waiting_for_user_issue)
async def create_request(message: types.Message, state: FSMContext):
    await state.finish()
    print(f'Текст обращения: {message.text}')
    user_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    request = ji.create_issue_tt(message.text, f"Запрос помощи от {user_name}", message.from_user.username)
    await message.bot.send_message(config.chat_id, f'Текст запроса от {user_name}: {message.text}')
    await message.bot.send_message(message.from_user.id, f'Ваша заявка принята. Номер заявки: "{request}"\n'
                                   'Спасибо за обращение!', reply_markup=kb.requests_kb)
    HBotBD.create_new_issue(message.from_user.id, 'Bitrix', config.docav, message.text, request)


@dp.message_handler(state=UserAnswers.waiting_for_issue_number, content_types=['text'])
async def issue_status(message: types.Message, state: FSMContext):
    await state.finish()
    await message.bot.send_message(config.chat_id, f'Поступил запрос статуса задачи номер {message.text} '
                                                   f'от пользователя username: @{message.from_user.username}\n'
                                                   f'Имя: {message.from_user.first_name} '
                                                   f'{message.from_user.last_name}')
    status = ji.status_of_issue(message.text)
    await message.answer(status, reply_markup=kb.requests_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
