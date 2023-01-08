
class AppException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# ----------------------------------------
# General
# ----------------------------------------
class ArgError(AppException):
    pass


class ExitMenuException(AppException):
    pass


# ----------------------------------------
# Database
# ----------------------------------------
class DuplicatedError(AppException):
    def __init__(self, key):
        super().__init__(f'{key} already exist')
        self.duplicated_key = key

class NotFoundError(AppException):
    def __init__(self, key):
        super().__init__(f'{key} didn\'t exist')
        self.notfound_key = key

class PermissionError(Exception):
    pass