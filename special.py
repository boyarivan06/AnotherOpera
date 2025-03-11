import functools
import logging

logging.basicConfig(filename = 'app.log', level = logging.INFO, format = '%(asctime)s -  %(levelname)s - %(message)s')

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Вызов функции: {str(func).split()[1]} с аргументами: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Функция {str(func).split()[1]}  выполнена успешно")
            return result
        except Exception as e:
            logging.error(f"Ошибка в функции {str(func).split()[1]}: {str(e)}", exc_info = True)
            raise
    return wrapper


class MetaControl(type):
    def __new__(cls, *args, **kwargs):
        with open('classes.txt', 'ra') as file:
            classes = file.readlines()
            if cls.__name__ not in classes:
                file.write(cls.__name__+'\n')
        return type.__new__(cls, *args, **kwargs)
