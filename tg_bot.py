from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from config import TG_BOT_TOKEN
from models import Track, Album, Artist


bot = TeleBot(TG_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Привет, я бот проекта Another Opera\n'
          'Найдите песню по артисту, альбому или названию, '
          'используя команды  /search_track')  # /search_artist, /search_album,

@bot.message_handler(commands=['search_artist', 'search_album', 'search_track'])
def start_search(msg):
    cls = None
    match msg.text.split('_')[-1]:
        case 'artist':
            cls = Artist
        case 'album':
            cls = Album
        case 'track':
            cls = Track
    bot.send_message(msg.chat.id, 'Введите текст поиска')
    bot.register_next_step_handler(msg, search, cls)

def search(msg, cls):
    data = cls.get_all(namesearch=msg.text)
    btns = [KeyboardButton(obj.name) for obj in data]
    markup = ReplyKeyboardMarkup()
    markup.add(*btns)
    bot.send_message(msg.chat.id, text="Выберите песню из предложенных", reply_markup=markup)
    bot.register_next_step_handler(msg, get_object, cls)


def get_object(msg, cls):
    result = cls.get_one(name=msg.text)
    bot.delete_message(msg.chat.id, msg.id-1)
    bot.delete_message(msg.chat.id, msg.id)
    bot.send_audio(msg.chat.id, result.audio, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def text(msg):
    pass