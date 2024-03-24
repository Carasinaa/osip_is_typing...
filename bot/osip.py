import telebot
import config
from telebot import types
from rhymes import findrhyme, rhymes, check_pair
import json
from stats import lines
from stats import titles
bot = telebot.TeleBot(config.TOKEN)

vowels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
pairs = [['б', 'п'], ['в', 'ф'], ['г', 'к'], ['з', 'с'], ['д', 'т']]
suitable_words = []
with open('morphs.json', 'r', encoding='utf-8') as f:
    morphs = json.load(f)
with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)


keyboard = types.InlineKeyboardMarkup()
osip_info = types.InlineKeyboardButton(text="Что ты такое?", callback_data="osip_info")
osip_rhymes = types.InlineKeyboardButton(text="Хочу рифмовать!", callback_data="osip_rhymes")
osip_history = types.InlineKeyboardButton(text="Кто такой Мандельштам?", callback_data="osip_history")
osip_help = types.InlineKeyboardButton(text="Мне нужна помощь!", callback_data="osip_help")
osip_stats = types.InlineKeyboardButton(text="Хочу посмотреть статистику", callback_data="osip_stats")
keyboard.add(osip_info)
keyboard.add(osip_rhymes)
keyboard.add(osip_history)
keyboard.add(osip_help)
keyboard.add(osip_stats)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Я -- Осип, бот, отвечающий на ваше сообщение строчкой из"
                                      " творчества Осипа Мандельштама!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "osip_info":
            bot.send_message(call.message.chat.id, "Я -- бот, отвечающий на сообщение строчкой Мандельштама. "
                                                   "Нажмите на кнопку 'Хочу рифмовать!' и введите предложение, "
                                                   "на которую я выдам строчку в рифму.", reply_markup=keyboard)
        if call.data == "osip_history":
            photo = open('osip.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(call.message.chat.id, "Осип Эмильевич Мандельштам (14 января 1891 -- 27 декабря 1938) "
                                                   "-- русский поэт, прозаик"
                                                   " и переводчик серебряного века, жертва сталинских репрессий. "
                                                   "Является одним из представителей литературного движения акмеистов, "
                                                   "куда входили также Ахматова и Гумилев. "
                                                   "Если вас заинтересовало творчество Мандельштама или акмеистическое"
                                                   " движение в целом, то можно почитать также и их работы и эссе.", reply_markup=keyboard)
        if call.data == "osip_help":
            bot.send_message(call.message.chat.id, "Если что-то не работает или работает, но не так, как нужно, "
                                                   "то свяжитесь с @carasinaa", reply_markup=keyboard)
        if call.data == 'osip_rhymes':
            bot.send_message(call.message.chat.id, "Пожалуйста,введите сообщение, на которое я выдам рифму!")

        if call.data == 'osip_stats':
            poses = open('poses.png', 'rb')
            words = open('wordcloud.png', 'rb')
            bot.send_message(call.message.chat.id, f"Количество строк: {lines}\nКоличество стихов: {titles}")
            bot.send_photo(call.message.chat.id, poses, 'Части речи, на которые чаще всего рифмуют')
            bot.send_photo(call.message.chat.id, words, 'Наиболее часто встречающиеся в стихах слова', reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def sendrhyme(message):
    text = message.text
    user = message.chat.id
    rhyme = findrhyme(text)
    bot.send_message(user, rhyme)
    bot.send_message(user, 'Пожалуйста, нажмите какую-нибудь кнопку!', reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
