class NotificatedUser:
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print(f"{self.name} получено сообщение: `{message}`")


class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)


class UserDataBase:
    _user_list = []
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def append(self, other):
        self._user_list.append(other)

    def __str__(self):
        return ', '.join([str(e) for e in self._user_list])

    def __iter__(self):
        return iter(self._user_list)


class NotificatedAdmin(NotificatedUser):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"Admin {self.name}"


class Developer(NotificatedUser):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"Proger {self.name}"

class UserFactory:
    @staticmethod
    def create_user(user_type, name):
        if user_type == "admin":
            return NotificatedAdmin(name)
        elif user_type == "developer":
            return Developer(name)


class UserManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self):
        return self.strategy.do_action(self)


class DevStrategy:
    def do_action(self):
        return f"I'm a programmer and C is the best language in the woaphaphapah..."


class AdminStrategy:
    def do_action(self):
        return f"I'm an admin, bi"
