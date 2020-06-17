import telebot
import toxic_bot_dao as dao
import toxic_bot_constants as const

bot = telebot.TeleBot(const.TELEGRAM_TOKEN)
bot.set_webhook(const.URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    chat_id = message.chat.id
    username_lower = str(user.username).lower()
    last_name_lower = str(user.last_name).lower()
    first_name_lower = str(user.first_name).lower()
    if username_lower == 'faleksander':
        bot.send_message(chat_id, 'Доброго времени суток, хозяин!')
    elif username_lower == 'taraskinnik':
        bot.send_message(chat_id, 'Ебать ты жирный ' + const.EMOJI_SCARED)
    elif username_lower == 'olga_gr':
        bot.send_message(chat_id, 'Привет, Оля!')
    elif username_lower == 'enqcore':
        bot.send_message(chat_id, 'Konnichiwa :3')
        bot.send_sticker(chat_id, const.STICKER_ANIME_CHAN_KONNICHIWA)
    elif username_lower == 'koshekans':
        bot.send_message(chat_id, 'Доброго, камрад!')
        bot.send_sticker(chat_id, const.STICKER_YOBA)
    elif username_lower == 'krutique':
        bot.send_message(chat_id, 'Приветствую, Ваше Татьяносство!')
    elif 'кузьмин' in last_name_lower:
        bot.send_message(chat_id, 'Падла ' + const.EMOJI_ANGRY)
    elif 'ksenia' in first_name_lower or 'vetrova' in last_name_lower:
        bot.send_photo(chat_id, open('files/raccoon_welcome.jpg', 'rb'))
    else:
        bot.send_message(chat_id, 'Вечер в хату!')
    bot.send_message(chat_id, 'Можешь использовать команду /bet чтобы поставить на следующего успешого съебатора!')
    if not dao.get_data(chat_id):
        dao.put_data(chat_id, user)


@bot.message_handler(commands=['bet'])
def handle_bet(message):
    chat_id = message.chat.id
    data = dao.get_data(chat_id)
    if not data:
        bot.send_message(chat_id, 'Сначала нада жмакнуть /start')
        return

    if dao.has_bets(chat_id):
        bot.send_message(chat_id, 'У тебя уже есть ставка ' + const.EMOJI_VERY_ANGRY)
        return

    split = str(message.text).split()
    if len(split) > 1:
        bet_username = None
        arg = split[1]
        if arg.isdigit():
            index = int(arg)
            if index < len(const.BET_USERNAME_DICT):
                bet_username = list(const.BET_USERNAME_DICT.items())[index][0]
        elif arg in const.BET_USERNAME_DICT:
            bet_username = arg
        else:
            bot.send_message(chat_id, 'Куда-то не туда ставишь :( Попробуй /bet <username>')
            bot.send_message(chat_id, 'Типа список: ' + ', '.join(const.BET_USERNAME_DICT.keys()))
            return

        dao.put_bet(chat_id, bet_username)
        bot.send_message(chat_id, 'Принято ' + const.EMOJI_SUNGLASSES + ' Смотри в /rates')
    else:
        if not bool(data.get(dao.ATTRIBUTE_USED_BET, None)):
            bot.send_photo(chat_id, open('files/faktura_whos_next.jpg', 'rb'))
            bot.send_audio(chat_id, open('files/faktura_kombat_short.mp3', 'rb'))
            dao.set_used_bet(chat_id)

        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        for item in list(const.BET_USERNAME_DICT.items()):
            markup.add(telebot.types.KeyboardButton('/bet ' + str(const.KEY_TO_POS[item[0]]) + ' ' + item[1]))
        bot.send_message(chat_id, 'Выбирай:', reply_markup=markup)


@bot.message_handler(commands=['rates'])
def handle_rates(message):
    bets = dao.get_all_bets()
    count = 0
    rates = {}
    for bet in bets:
        user_name = bet[dao.ATTRIBUTE_BET_USER_NAME]
        rates[user_name] = rates.get(user_name, 0) + 1
        count += 1

    res = ''
    for key in rates.keys():
        res += const.BET_USERNAME_DICT[key] + ' - ' + ("%.2f" % (rates[key] / count * 100)) + '%\n'

    bot.send_message(message.chat.id, res)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    bot.reply_to(message, message.text)


def process(json):
    de_json = telebot.types.Update.de_json(json)
    if de_json is not None:
        bot.process_new_messages([de_json.message])
