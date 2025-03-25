from .tg_bot import bot


def main():
    bot.polling(non_stop=True)
