import telebot
import config  # Все что не связанно непосредственно с работой бота

bot = telebot.TeleBot(config.token_bot)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Разработки и доработки', 'Помощь в офисе')
keyboardIT = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardIT.row('Ответ на запрос')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Используйте клавиатуру для навигации по функциям бота.',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.text.lower() == "разработки и доработки":
        print(f'Обращение по разработке от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        config.request_type = 0
        send = bot.send_message(message.from_user.id, 'Что необходимо реализовать и в какой области?')
        bot.send_message(config.chat_id, f'Поступил запрос на разработку от '
                                         f'{message.from_user.first_name} {message.from_user.last_name}, '
                                         f'ожидайте последующего сообщения с информацией')
        bot.register_next_step_handler(send, help_request)
    if message.text.lower() == "помощь в офисе":
        print(f'Обращение по помощи от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        config.request_type = 1
        send = bot.send_message(message.from_user.id, 'Опишите свою проблему')
        bot.send_message(config.chat_id, f'Поступил запрос помощи от '
                                         f'{message.from_user.first_name} {message.from_user.last_name}, '
                                         f'ожидайте последующего сообщения с информацией')
        bot.register_next_step_handler(send, help_request)
    if message.text.lower() == "ответ на запрос":
        print('IT отдел ответил на запрос: тут номер запроса')
        bot.send_message(config.chat_id, 'Пока не готова функция, ожидайте', reply_markup=keyboardIT)
        """Ну и сюда потом код для ответа"""


def help_request(message):
    print(f'Текст обращения: {message.text}')
    user_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.from_user.id, 'Ваша заявка принята, ожидайте ответа от IT отдела', reply_markup=keyboard1)
    bot.send_message(config.chat_id, f'{user_name} отправил запрос: {message.text}')
    if config.request_type == 0:
        config.create_issue(message.text, f'Доработка от {user_name}', message.from_user.username)
    else:
        config.create_issue(message.text, f'Запрос помощи от {user_name}', message.from_user.username)


bot.infinity_polling()
