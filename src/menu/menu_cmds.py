import string
from typing import Any

import controller.controller as controller
from command.command import Command
from model.database import Database
from model.data_type import User, Sheet
from permission.permission import Permission, PermissionFactory


class ArgumentError(Exception):
    pass

class ExitMenuException(Exception):
    pass


def less_dangerous_eval(equation):
    if not set(equation).intersection(string.ascii_letters + '{}[]_;\n'):
        return eval(equation)
    else:
        raise ArgumentError('illegal input')


class CreateUser(Command):
    def brief_description(self) -> str:
        return """Create a user"""

    def help(self) -> str:
        return """input a user name to create a user"""


    def execute(self, args: tuple) -> Any:
        name = input('user name:\n>')
        controller.create_user(name)
        print(f"Create user {name}.")


class CreateSheet(Command):
    def brief_description(self) -> str:
        return """Create a sheet"""

    def help(self) -> str:
        return """input user name and sheet name to create a sheet"""


    def execute(self, args: tuple) -> Any:
        username, sheet_name = input('user_name sheet_name:\n>').split(' ')
        controller.create_sheet(username, sheet_name)
        print(f"Create a sheet {sheet_name} for user {username}.")


class CheckSheet(Command):
    def brief_description(self) -> str:
        return """Check a sheet"""

    def help(self) -> str:
        return """input user name and sheet name to check a sheet"""


    def execute(self, args: tuple) -> Any:
        username, sheet_name = input('user_name sheet_name:\n>').split(' ')
        sheet = controller.create_sheet(username, sheet_name)
        print(sheet)


class EditSheetValue(Command):
    def brief_description(self) -> str:
        return """Edit a sheet"""

    def help(self) -> str:
        return """input user name and sheet name to edit a sheet"""

    def execute(self, args: tuple) -> Any:
        username, sheet_name = input('user_name sheet_name:\n>').split(' ')

        sheet = controller.get_sheet(username, sheet_name)
        print(sheet)

        row, col, val = input("please input (row, col, val):\n>").split(' ')
        row = int(row)
        col = int(col)
        val = less_dangerous_eval(val)

        controller.edit_sheet(username, sheet_name, row, col, val)

        print(f"Edit sheet {sheet_name} success")


class EditPermission(Command):
    def brief_description(self) -> str:
        return """Edit a sheet's access right"""

    def help(self) -> str:
        return """"""


    def execute(self, args: tuple) -> Any:
        username, sheet_name, per_str = input('user_name sheet_name permission(ReadOnly/Editable):\n>').split(' ')

        match per_str:
            case 'ReadOnly':
                permission = PermissionFactory.readonly()
            case 'Editable':
                permission = PermissionFactory.editable()
            case _:
                raise ArgumentError("Input can only be `ReadOnly` or `Editable`")
            
        controller.edit_permission(username, sheet_name, permission)
        print(f"user{username} to sheet{sheet_name} is set to {permission}")


class ShareToUser(Command):
    def brief_description(self) -> str:
        return """Collaborate with an other user."""

    def help(self) -> str:
        return """enter the user name, sheet name and target user name"""

    def execute(self, args: tuple) -> Any:
        username, sheet_name, target_name = input('user_name sheet_name target_user:\n>').split(' ')
        controller.share_permission(username, sheet_name, target_name)    
        print(f"share sheet {sheet_name} from user {username} to {target_name}")


class ExitMenu(Command):
    def brief_description(self) -> str:
        return """Exit Menu"""

    def help(self) -> str:
        return """Exit Menu uwu"""

    def execute(self, args: tuple) -> Any:
        raise ExitMenuException()
