import telebot
import os
from extensions import APIException, Convertor


# Currency config file parser. Currencies in format 'Name:Code'
def config_parser(text):
    temp_dict = {}
    lines = text.split()
    for i in lines:
        temp_dict.update([tuple(i.split(':'))])
    return temp_dict


# Loading currencies
file_path = os.getcwd()
config_file = open('config.txt', 'r')
currencies = config_parser(config_file.read())
config_file.close()

# Loading token from file stored higher at file tree
os.chdir('..')
# file_path = os.getcwd()
token_file = open('sqmax_bot_token.txt', 'r', encoding='utf8')
TOKEN = token_file.read()
token_file.close()
bot = telebot.TeleBot(TOKEN)


# Greeting message
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Greetings!")


# Commands list
@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"/values - list of available currencies\n"
                                      f"<base Currency1> <quote Currency2> <amount of Currency1>")


# Currency list message
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for i in currencies.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


# Conversion request message
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    val = message.text.split(' ')
    try:
        if len(val) != 3:
            raise APIException('Wrong arguments amount')
        answer = Convertor.get_price(*val, currencies)

    except APIException as e:
        bot.reply_to(message, f'Command error:\n{e}\ntype /help for instructions')

    except Exception as e:
        bot.reply_to(message, f'Unknown error:\n{e}\ntype /help for instructions')

    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
