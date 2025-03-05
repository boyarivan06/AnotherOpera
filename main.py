import prompt

from models.base import Artist
from models.base import Song


def main():
    data = dict()
    message = '''1 - добавить песню
2 - изменить песню
3 - удалить песню
4 - вывести песни
0 - завершить
    '''
    print(message)
    while True:
        up = False
        cmd = prompt.integer("* Введите команду: ", 5)
        if cmd == 1:
            name = prompt.string("Введите название: ")
            artist = Artist(name=prompt.string("Введите исполнителя: "))
            if name in data:
                print("Такая запись уже есть")
                continue
            data[name] = Song(name=name, artist=artist, record='albummm', duration=2.43)
            print('Успешно')
        elif cmd == 2:
            name = prompt.string("Введите название песни: ")
            while name not in data:
                name = prompt.string("Такой записи нет, попробуйте ещё или "
                                     "введите 0, чтобы выйти в меню: ")
                if name == '0':
                    up = True
                    break
            if up:
                continue
            par = prompt.string("Введите параметр для замены (name, artist, record): ")
            while par not in ['name', 'artist', 'record']:
                par = prompt.string("Ошибка, введите параметр для замены "
                                    "(name, artist, record), 0 для выхода в меню: ")
                if name == '0':
                    up = True
                    break
            if up:
                continue
            value = prompt.string('Введите новое значение: ')
            data[name].__dict__[par] = value
        elif cmd == 3:
            name = prompt.string("Введите название песни: ")
            while name not in data:
                name = prompt.string("Такой записи нет, попробуйте "
                                     "ещё или введите 0, чтобы выйти в меню: ")
                if name == '0':
                    up = True
                    break
            if up:
                continue
            confirm = prompt.character('Подтвердите удаление (y/n): ')
            if confirm.lower() == 'y':
                del data[name]
                print('Успешно')
        elif cmd == 4:
            print(*[f'{data[k].name} by {data[k].artist} from record {data[k].record}'
                    for k in data], sep='\n')
        else:
            print("До встречи")
            return 0

if __name__ == "__main__":
    main()
