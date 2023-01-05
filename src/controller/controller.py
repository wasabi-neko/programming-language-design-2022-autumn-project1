from user_sheet.usersheet import User, Sheet
from user_sheet.database import Database
from permission.permission import PermissionFactory, Permission


def create_user(user_name: str) -> None:
    Database.get_instance().add_user(user_name)


def get_user(user_name: str) -> User:
    return Database.get_instance().get_user_by_name(user_name)


def create_sheet(user_name: str, sheet_name: str):
    permission = PermissionFactory.owner()
    Database.get_instance().new_sheet(user_name, sheet_name, permission)


def get_sheet(user_name: str, sheet_name: str) -> Sheet:
    sheet = Database.get_instance().check_sheet(user_name, sheet_name)
    return sheet


def update_sheet(user_name: str, sheet_name: str, new_sheet: Sheet):
    Database.get_instance().update_sheet(user_name, sheet_name, new_sheet)


def edit_sheet(user_name: str, sheet_name: str, row: int, col: int, val: int):
    db = Database.get_instance()
    sheet = db.check_sheet(user_name, sheet_name)
    sheet.edit_sheet(row, col, val)
    db.update_sheet(user_name, sheet_name, sheet)


def edit_permission(user_name: str, sheet_name: str, permission: Permission):
    db = Database.get_instance()
    user = db.get_user_by_name(user_name)
    sheet = db.get_sheet_by_name(sheet_name)
    db.edit_permission(user, sheet, permission)


# TODO: can someone override the permission that already exist??
def share_permission(user_name: str, sheet_name: str, target_name: str):
    db = Database.get_instance()
    user = db.get_user_by_name(user_name)
    target = db.get_user_by_name(target_name)
    sheet = db.get_sheet_by_name(sheet_name)
    permission = db.get_permission(user, sheet)
    shared_permission = permission.max_share()
    db.edit_permission(target, sheet, shared_permission)
