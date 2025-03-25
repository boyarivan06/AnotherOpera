from typing import Type

from telebot import TeleBot
from telebot.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from config import TG_BOT_TOKEN
from utils.api import APIConnect
from utils.custom_exc import APIFailException
from utils.models import Album, Artist, Track

bot = TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(msg: Message) -> None:
    """
    Начало работы с ботом
    :param msg: команда пользователя
    """
    bot.send_message(
        msg.chat.id,
        "Привет, я бот проекта Another Opera\n"
        "Найдите песню по артисту, альбому или названию, "
        "используя команды /search_artist, /search_album, /search_track",
    )


@bot.message_handler(commands=["search_artist", "search_album", "search_track"])
def start_search(msg: Message) -> None:
    """
    Начало поиска
    :param msg: команда пользователя
    """
    cls = None
    match msg.text.split("_")[-1]:
        case "artist":
            cls = Artist
        case "album":
            cls = Album
        case "track":
            cls = Track
    bot.send_message(msg.chat.id, "Введите текст поиска")
    bot.register_next_step_handler(msg, search, cls)


def search(msg: Message, cls: Type[APIConnect]) -> None:
    """
    Поиск по введённому запросу в соответствующей таблице.
    Выдаёт клавиатуру с названиями найденных элементов
    :param msg: запрос
    :param cls: класс модели API
    """
    data = cls.get_all(namesearch=msg.text)
    btns = [KeyboardButton(obj.name) for obj in data]
    markup = ReplyKeyboardMarkup()
    markup.add(*btns)
    bot.send_message(
        msg.chat.id, text="Выберите название из предложенных", reply_markup=markup
    )
    bot.register_next_step_handler(msg, get_object, cls)


def get_object(msg: Message, cls: Type[APIConnect]) -> None:
    """
    Возвращает найденный элемент в зависимости от типа: Artist - список альбомов,
    Album - список песен, Track - песню для прослушивания
    :param msg:
    :param cls:
    """
    result = None
    try:
        result = cls.get_one(name=msg.text)
    except APIFailException or not result:
        bot.send_message(msg.chat.id, f"Ничего не найдено по запросу `{msg.text}`")
        return
    bot.delete_message(msg.chat.id, msg.id - 1)
    bot.delete_message(msg.chat.id, msg.id)
    if cls == Track:
        bot.send_audio(
            msg.chat.id,
            result.audio,
            caption=f"{result.name} by {result.artist_name}",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif cls == Album:
        data = Track.get_all(album_id=result.id, limit="all")
        btns = [KeyboardButton(obj.name) for obj in data]
        markup = ReplyKeyboardMarkup()
        markup.add(*btns)
        bot.send_photo(
            msg.chat.id,
            result.image,
            caption=f"{result.name} by {result.artist_name}",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, get_object, Track)
    elif cls == Artist:
        data = Album.get_all(artist_id=result.id, limit="all")
        btns = [KeyboardButton(obj.name) for obj in data]
        markup = ReplyKeyboardMarkup()
        markup.add(*btns)
        bot.send_photo(
            msg.chat.id, result.image, caption=f"{result.name}", reply_markup=markup
        )
        bot.register_next_step_handler(msg, get_object, Album)
