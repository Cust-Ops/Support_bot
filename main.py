import telebot
import config  # Все что не связанно непосредственно с работой бота

bot = telebot.TeleBot(config.token_bot_main)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Помощь с Bitrix', 'Помощь в офисе')
keyboardyn = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardyn.row('Да', 'Нет')


# Стартовое сообщение для пользователей
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в бота технической поддержки. Чтобы создать заявку, '
                                           'выберите кнопку "Помощь с Bitrix" или "Помощь в офисе" на клавиатуре бота. '
                                           'Если вы не видите клавиатуру бота, нажмите иконку в виде плитки, она '
                                           'находится в текстовом поле справа.'
                                           'Обучающий материал вы можете найти по ссылке: https://clck.ru/WSVdf',
                     reply_markup=keyboard1)


# Проверка на вид запроса от пользователя
@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.text.lower() == "помощь в bitrix":
        print(f'Обращение по помощи от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        send = bot.send_message(message.from_user.id, 'Вы хотите приложить скриншот или документ к запросу? Для ответа '
                                                      'воспользуйтесь клавиатурой бота', reply_markup=keyboardyn)
        bot.send_message(config.chat_id, f'Поступил запрос помощи от '
                                         f'{message.from_user.first_name} {message.from_user.last_name}, '
                                         f'ожидайте последующего сообщения с информацией')
        bot.register_next_step_handler(send, take_a_picture)
    elif message.text.lower() == "помощь в офисе":
        print(f'Обращение по помощи от пользователя username: @{message.from_user.username}\n'
              f'Имя: {message.from_user.first_name} {message.from_user.last_name}')
        send = bot.send_message(message.from_user.id, 'Вы хотите приложить скриншот или документ к запросу? Для ответа '
                                                      'воспользуйтесь клавиатурой бота', reply_markup=keyboardyn)
        bot.send_message(config.chat_id, f'Поступил запрос помощи от '
                                         f'{message.from_user.first_name} {message.from_user.last_name}, '
                                         f'ожидайте последующего сообщения с информацией')
        bot.register_next_step_handler(send, take_a_picture)
    else:
        bot.send_message(message.from_user.id, 'Вы совершили ошибку при использовании бота. Пожалуйста перед '
                                               'созданием запроса, используйте клавиатуру бота.'
                                               'Обучающий материал вы можете найти по ссылке: https://clck.ru/WSVdf')


def take_a_picture(message):
    if message.text.lower() == "да":
        print(f'К запросу приложен документ')
        config.request_type = 1
        send = bot.send_message(message.from_user.id, 'Отправьте желаемый файл')
        bot.register_next_step_handler(send, take_a_picture_y)
    if message.text.lower() == "нет":
        config.request_type = 0
        send = bot.send_message(message.from_user.id, 'Опишите вашу проблему. Помните, '
                                                      'что ваш запрос должен быть оформлен в одном сообщении!')
        bot.register_next_step_handler(send, help_request)


@bot.message_handler(content_types=['document'])
def take_a_picture_y(message):
    send = bot.send_message(message.from_user.id, 'Документ приложен. Теперь опишите свою проблему. Помните, что '
                                                  'ваш запрос должен быть оформлен в одно сообщение.')
    """ Скачивание файла. Задел на будущее
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        global src
        src = 'C:/Users/Admin/Documents/PyProject/TeleBot/doc/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as e:
        bot.reply_to(message, 'Не сжимайте отправляемый файл. Уберите галочку "Сжимать файл" при загрузке файла и '
                              'создайте новый запрос.'
                              'Обучающий материал вы можете найти по ссылке: https://clck.ru/WSVdf')
        print(e)
    """
    bot.forward_message(config.chat_id, message.chat.id, message.message_id)
    """bot.send_document(config.chat_id,
                      open(src, 'rb'))"""
    bot.register_next_step_handler(send, help_request)


def help_request(message):
    print(f'Текст обращения: {message.text}')
    user_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.from_user.id, 'Ваша заявка принята. Спасибо за обращение!', reply_markup=keyboard1)
    bot.send_message(config.chat_id, f'Текст запроса от {user_name}: {message.text}')
    if config.request_type == 0:
        config.create_issue_ttn(message.text, f'Запрос помощи в Bitrix от {user_name}', message.from_user.username)
    else:
        config.create_issue_tty(message.text, f'Запрос помощи от {user_name}',
                                message.from_user.username)


if __name__ == '__main__':
    bot.infinity_polling()
