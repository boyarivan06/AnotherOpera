class DurationException(BaseException):
    def __init__(self, message="Некорректная длительность композиции"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class APIFailException(BaseException):
    def __init__(self, message="Ничего не найдено по запросу"):
        self.message = message

    def __str__(self):
        return self.message
