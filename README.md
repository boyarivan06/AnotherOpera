# Проект "Другая опера"

## Описание проекта
Приложение и бот для поиска и прослушивания музыки с сервиса [Jamendo](https://www.jamendo.com/?language=ru).
## Функциональные требования
Приложение с графическим интерфейсом, позволяющее производить поиск и прослушивание музыки. Бот с аналогичным функционалом.
## Технические требования
* Python>=3.10
* Poetry
* PyQt5
* PyTelegramBotApi
## Структура проекта
```
.
├── Makefile
├── QT_windows
│     ├── confirm.ui
│     ├── main.ui
│     ├── new_song.ui
│     ├── select_song.ui
│     └── song_view.ui
├── README.md
├── __pycache__
│     └── config.cpython-313.pyc
├── app
│     ├── __init__.py
│     ├── __pycache__
│     │     ├── __init__.cpython-313.pyc
│     │     └── interface.cpython-313.pyc
│     ├── interface.py
│     └── main.py
├── app.log
├── bot
│     ├── __init__.py
│     ├── main.py
│     └── tg_bot.py
├── config.py
├── dist
│     ├── another opera-0.1.0-py3-none-any.whl
│     └── another opera-0.1.0.tar.gz
├── poetry.lock
├── pyproject.toml
├── screenshots
│     ├── app1.png
│     ├── app2.png
│     ├── tg1.png
│     ├── tg2.png
│     └── tg3.png
└── utils
    ├── __init__.py
    ├── api.py
    ├── custom_exc.py
    ├── models.py
    └── special.py

```
## Объяснение структуры проекта
* app - исходный код приложения
* QT_windows - файлы UI для приложения
* bot - исходный код бота
* screenshots - снимки экрана для этого README
* utils - исходный код утилит API, логирования, моделей
* Makefile - 

## Инструкция по установке, настройке и запуску проекта
#### Установка:
1. `make install`
2. `make build`
#### Запуск
`make run`

#### Запуск отдельно бота или приложения
`make bot` или `make app`

#### Проверка чистоты кода
`make lint`

## Пример использования
#### Приложение
Пользуясь строкой поиска, находим артиста, выбираем в соответствующих окнах альбом и песню. Нажимаем `PLAY`. Пока слушаем, можно выбрать следующую песню.
#### Бот
Одной из команд `/search_artist`, `/search_album`, `/search_track` по артисту, альбому или названию находим песню и слушаем в Telegram.
## Скриншоты, подтверждающие работоспособность проекта
![](screenshots/app1.png)
![](screenshots/app2.png)
![](screenshots/tg1.png)
![](screenshots/tg2.png)
![](screenshots/tg3.png)

## Источники
[Бесплатный музыкальный сервис Jamendo](https://www.jamendo.com/?language=ru)