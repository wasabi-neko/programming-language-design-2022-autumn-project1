from __future__ import annotations
from typing import TypeVar, Generic
import copy, functools

from permission.permission import Permission, PermissionError
from model.data_type import User, Sheet
from exceptions.exceptions import ArgError, DuplicatedError, NotFoundError



def not_null_str(arg: str):
    if type(arg) != str:
        raise ArgError("input type must be string")
    if len(arg) <= 0:
        raise ArgError("length of input string must greater than 0")
    if arg.count(' ') > 0:
        raise ArgError("input cannot contain space character")
    return arg


def arg_check(*validators):
    """return a decorator"""
    def decorator(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            n = len(validators)
            for (arg, validator) in zip(args[:n], validators):
                validator(arg)
            return func(*args, **kwargs)
        return wrap
    return decorator


def method_arg_check(*validators):
    return arg_check(lambda x: True, *validators)



KT = TypeVar('KT')
VT = TypeVar('VT')

class SafeDict(Generic[KT, VT]):
    """A data-structure extended from `dict`, which has more restrict access method and type checking
    """
    data: dict[KT, VT]

    def __init__(self, d: dict[KT, VT]) -> None:
        self.data = d
    
    def __str__(self) -> str:
        return f"SafeDict[{KT}{VT}]: {self.data}"
    
    def get(self, key: KT) -> VT:
        return self.data[key]
    
    def add(self, new_key: KT, val: VT) -> None:
        if new_key in self.data:
            raise DuplicatedError(new_key)
        self.data[new_key] = val
    
    def remove(self, key: KT):
        self.data.pop(key)
    
    def edit(self, key: KT, val: VT) -> None:
        if key not in self.data:
            raise NotFoundError(key)
        self.data[key] = val
    
    def has_key(self, key: KT) -> bool:
        return key in self.data


class Database():
    """Use singleton
    """

    # class variables
    _instance: Database|None = None

    # instance variables
    users: SafeDict[str, User]
    sheets: SafeDict[str, Sheet]
    table: SafeDict[tuple[User, Sheet], Permission]


    @classmethod
    def get_instance(cls) -> Database:
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def __init__(self) -> None:
        assert Database._instance is None, "class Database is a singleton. __init__ can not be called after _instance already exist"

        self.users = SafeDict({})
        self.sheets = SafeDict({})
        self.table = SafeDict({})

    # ----------------------------------------
    # Users methods
    # ----------------------------------------
    @method_arg_check(not_null_str)
    def get_user_by_name(self, name: str) -> User:
        return self.users.get(name)

    
    @method_arg_check(not_null_str)
    def add_user(self, username: str):
        user = User(username)
        self.users.add(username, user)
    

    @method_arg_check(not_null_str)
    def rm_user_by_name(self, name: str):
        self.users.remove(name)

    # ----------------------------------------
    # Sheets methods
    # ----------------------------------------
    @method_arg_check(not_null_str)
    def get_sheet_by_name(self, name: str) -> Sheet:
        return self.sheets.get(name)


    @method_arg_check(not_null_str, not_null_str)
    def new_sheet(self, username: str, sheet_name: str, permission: Permission) -> None:
        user = self.users.get(username)
        sheet = Sheet(sheet_name)
        self.sheets.add(sheet_name, sheet)
        self._insert(user, sheet, permission)
    

    @method_arg_check(not_null_str, not_null_str)
    def check_sheet(self, username: str, sheet_name: str) -> Sheet:
        user = self.users.get(username)
        sheet = self.sheets.get(sheet_name)

        try:
            permission = self.table.get((user, sheet))
        except:
            raise PermissionError("Permission denied")

        if not permission.is_readable():
            raise PermissionError("Permission denied")
        
        return copy.deepcopy(sheet)
    

    @method_arg_check(not_null_str, not_null_str)
    def update_sheet(self, username: str, sheet_name: str, new_sheet: Sheet) -> None:
        user = self.users.get(username)
        sheet = self.sheets.get(sheet_name)

        try:
            permission = self.table.get((user, sheet))
        except:
            raise PermissionError("Permission denied")

        if not permission.is_writeable():
            raise PermissionError("Permission denied")
        
        sheet.update_data(new_sheet)

        
    # ----------------------------------------
    # UserSheetTable methods
    # ----------------------------------------
    def _insert(self, user: User, sheet: Sheet, permission: Permission) -> None:
        self.table.add((user, sheet), permission)
    

    @method_arg_check(not_null_str, not_null_str)
    def edit_permission(self, username: str, sheet_name: str, permission: Permission) -> None:
        user = self.users.get(username)
        sheet = self.sheets.get(sheet_name)
        if self.table.has_key((user, sheet)):
            self.table.edit((user, sheet), permission)
        else:
            self.table.add((user, sheet), permission)

    @method_arg_check(not_null_str, not_null_str)
    def get_permission(self, username: str, sheet_name: str) -> Permission:
        user = self.users.get(username)
        sheet = self.sheets.get(sheet_name)
        return self.table.get((user, sheet))
    
    @method_arg_check(not_null_str, not_null_str)
    def get_permission_by_name(self, username: str, sheet_name: str) -> Permission:
        user = self.users.get(username)
        sheet = self.sheets.get(sheet_name)
        return self.table.get((user, sheet))
