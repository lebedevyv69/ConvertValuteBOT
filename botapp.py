import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConventer
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', 'info'])
def help(message: telebot.types.Message):
    text = "Приветствую,это бот для конвертации валют, чтобы начать работу с нашим ботом, ведите команды следущим образом:\n<название начальной с маленькой буквы валюты> \ <название валюты в которую нужно перевести тоже с маленькой буквы> " \
           "\ <количество переводимой валюты> "'\n Например: доллар рубль 100  ''\n Чтобы увидеть список доступных валют введите команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты на данный момент:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
            values=message.text.split(' ')

            if len(values) != 3:
                raise ConvertionException('Вы ввели неверные данные, чтобы узнать правила работы бота введите команду: /info')

            quote, base , amount = values
            total_base= CryptoConventer.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()
