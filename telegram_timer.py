import telebot
from telebot import types
import requests

BOT_TOKEN = '<API ТОКЕН БОТА>' # тут нужно вставить API токен бота
bot = telebot.TeleBot(BOT_TOKEN)


def get_my_content(url):
    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}
        return requests.get(url, headers=headers)
    except:
        return False


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        try:
            bot.send_message(message.from_user.id, 'Привет!\nНажми кнопку "ℹ Информация", чтобы получить актуальное число оставшихся блоков до халвинга Биктоина.', reply_markup = keyboard())
        except:
            pass
    else:
        try:
            bot.send_message(message.from_user.id, 'Загружаю данные...')
        except:
            pass
        # Получаем среднее время добычи блока.
        time_info = get_my_content(url='https://blockchain.info/q/interval')
        if time_info and time_info.status_code == 200:
            # Получаем кол-во добытых блоков.
            block_info = get_my_content(url='https://blockchain.info/q/getblockcount')
            # Проверяем доступ.
            if block_info and block_info.status_code == 200 and block_info.text.isdigit():
                # Получаем количество оставшихся блоков.
                blocks_left = 210000 - (int(block_info.text) % 210000)
                # Получаем сырое оставшееся время в секундах.
                raw_seconds = float(time_info.text) * blocks_left
                # Вычисляем дни.
                days_left = int(raw_seconds / 86400)
                # Вычисляем часы.
                hours_left = int(raw_seconds / 3600) - days_left * 24
                # Вычисляем минуты.
                minutes_left = int(raw_seconds / 60) - hours_left * 60 - days_left * 1440
                # Вычисляем секунды.
                seconds_left = int(raw_seconds) - minutes_left * 60 - hours_left * 3600 - days_left * 86400
                try:
                    bot.send_message(message.from_user.id, f'📦 Блоков до халвинга: {blocks_left}\n⏳ Осталось времени\nДней: {days_left:02}\nЧасов: {hours_left:02}\nМинут: {minutes_left:02}\nСекунд: {seconds_left:02}', reply_markup = keyboard())
                except:
                    pass
            else:
                try:
                    bot.send_message(message.from_user.id, 'Ой. Не смог понять сколько блоков осталось 😭')
                except:
                    pass
        else:
            bot.send_message(message.from_user.id, 'Ой. Я не смог определить среднее время добычи блока 😭')


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('ℹ Информация')
    markup.add(btn1)
    return markup


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, interval=0)
        print('start - ok')
    except:
        print('start - error')
