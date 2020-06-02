import os
import telebot

project_id_ = os.environ['GCP_PROJECT']
entry_point_ = os.environ['ENTRY_POINT']
function_region_ = os.environ['FUNCTION_REGION']
url_ = f'https://{function_region_}-{project_id_}.cloudfunctions.net/{entry_point_}'

bot = telebot.TeleBot(os.environ['TOKEN'])
bot.set_webhook(url_)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Здарова, Бандит!')


def process(json):
    bot.process_new_messages([telebot.types.Update.de_json(json).message])

