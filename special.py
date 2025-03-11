import functools
import logging

logging.basicConfig(filename = 'app.log', level = logging.INFO,
                    format = '%(asctime)s -  %(levelname)s - %(message)s')

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Вызов функции: {str(func).split()[1]} "
                     f"с аргументами: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Функция {str(func).split()[1]}  выполнена успешно")
            return result
        except Exception as e:
            logging.error(f"Ошибка в функции {str(func).split()[1]}: "
                          f"{str(e)}", exc_info = True)
            raise
    return wrapper


class MetaControl(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        with open('classes.txt', 'a+') as file:
            file.seek(0)  # Rewind to read existing content
            existing_classes = [line.strip() for line in file.readlines()]

            if name not in existing_classes:
                file.write(f"{name}\n")  # Write new line if class not exists

        return super().__new__(cls, name, bases, namespace, **kwargs)
