import telebot
import toxic_bot_constants as const

bot = telebot.TeleBot(const.TOKEN)
bot.set_webhook(const.URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private' and message.chat.username is not None and message.chat.username == 'faleksander1':
        bot.reply_to(message, 'Здарова, Бандит!')
        bot.send_sticker(message.chat.id, const.FRY_FUCK_YOU_STICKER, message.message_id)
    elif message.chat.last_name == 'Fal' or message.chat.last_name == 'Кузьмин':
        bot.reply_to(message, 'Падла')
    else:
        bot.send_sticker(message.chat.id, const.FRY_FUCK_YOU_STICKER, message.message_id)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    bot.reply_to(message, message.text)


def process(json):
    de_json = telebot.types.Update.de_json(json)
    if de_json is not None:
        bot.process_new_messages([de_json.message])
