import functools

from loguru import logger

logger.add(
    "../app.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    compression="zip",
)


def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            f"Вызов функции: {str(func).split()[1]} " f"с аргументами: {args}, {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            logger.info(f"Функция {str(func).split()[1]}  выполнена успешно")
            return result
        except Exception as e:
            logger.error(
                f"Ошибка в функции {str(func).split()[1]}: " f"{str(e)}", exc_info=True
            )
            raise

    return wrapper


class MetaControl(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        with open("../classes.txt", "a+") as file:
            file.seek(0)  # Rewind to read existing content
            existing_classes = [line.strip() for line in file]

            if name not in existing_classes:
                file.write(f"{name}\n")  # Write new line if class not exists

        return super().__new__(cls, name, bases, namespace, **kwargs)


class Descriptor(metaclass=MetaControl):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)
