import telebot
import config  # Переменные

bot = telebot.TeleBot(config.token_bot)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Зарегистрировать обращение')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Используйте клавиатуру для навигации по функциям бота.',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.text.lower() == "зарегистрировать обращение":
        print(f'Обращение от пользователя Логин: @{message.from_user.username}\nИмя: {message.from_user.first_name}'
              f' {message.from_user.last_name}')
        send = bot.send_message(message.from_user.id, "Опишите свою проблему")
        bot.send_message(config.chat_id, f'Поступило обращение в поддержу от '
                                         f'{message.from_user.first_name} {message.from_user.last_name}, '
                                         f'ожидайте последующего сообщения с информацией')
        bot.register_next_step_handler(send, help_request)


def help_request(message):
    print(f'Текст обращения {message}')
    user_name = f'Логин: @{message.from_user.username} имя: {message.from_user.first_name}' \
                f' {message.from_user.last_name}'
    bot.send_message(message.from_user.id, 'Ваша заявка принята, ожидайте ответа от IT отдела')
    bot.send_message(config.chat_id, f'{user_name} отправил запрос: {message.text}')
    # config.sql_work(1, message.from_user.first_name, message.from_user.last_name, 'Обращение в тех. поддержку', message)


bot.infinity_polling()
