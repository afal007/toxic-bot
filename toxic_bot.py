import telebot
import toxic_bot_constants as const

bot = telebot.TeleBot(const.TOKEN)
bot.set_webhook(const.URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user = message.from_user
        chat_id = message.chat.id
        username_lower = str(user.username).lower()
        last_name_lower = str(user.last_name).lower()
        first_name_lower = str(user.first_name).lower()
        if username_lower == 'faleksander':
            bot.send_message(chat_id, 'Доброго времени суток, хозяин!')
        elif 'кузьмин' in last_name_lower:
            bot.send_message(chat_id, 'Падла ' + const.EMOJI_ANGRY)
        elif username_lower == 'taraskinnik':
            bot.send_message(chat_id, 'Ебать ты жирный ' + const.EMOJI_SCARED)
        elif 'ksenia' in first_name_lower or 'vetrova' in last_name_lower:
            bot.send_photo(chat_id, open('files/raccoon_welcome.jpg', 'rb'))
        else:
            bot.send_message(chat_id, 'Вечер в хату!')
        bot.send_message(chat_id, 'Можешь заюзать команду /bet чтобы поставить на следующего успешого съебатора!')
    except AttributeError as e:
        print(e)
        bot.send_message(message.chat.id, 'Произошла хуйня :(')


@bot.message_handler(commands=['bet'])
def handle_bet(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, open('files/faktura_whos_next.jpg', 'rb'))
    bot.send_audio(chat_id, open('files/faktura_kombat_short.mp3', 'rb'))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    bot.reply_to(message, message.text)


def process(json):
    de_json = telebot.types.Update.de_json(json)
    if de_json is not None:
        bot.process_new_messages([de_json.message])
