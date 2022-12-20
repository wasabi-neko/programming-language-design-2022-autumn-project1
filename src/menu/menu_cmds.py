import string
from typing import Any

from command.command import Command
from user_sheet.database import Database
from user_sheet.usersheet import User, Sheet
from permission.permission import Permission, PermissionFactory


def less_dangerous_eval(equation):
    if not set(equation).intersection(string.ascii_letters + '{}[]_;\n'):
        return eval(equation)
    else:
        raise ValueError('illegal input')

class CreateUser(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Create a user"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """input a user name to create a user"""


    def execute(self, args: tuple) -> Any:
        print("user name: ", end='\n>')
        name = input()
        if len(name) <= 0:
            raise ValueError('user name cannot be none')

        Database.get_instance().add_user(name)

        print(f"Create user {name}.")
        return


class CreateSheet(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Create a sheet"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """input user name and sheet name to create a sheet"""


    def execute(self, args: tuple) -> Any:
        print("please enter: 'user_name sheet_name' ", end='\n>')
        username, sheet_name = input().split(' ')

        if len(sheet_name) <= 0:
            raise ValueError('sheet name cannot be none')

        permission = PermissionFactory.owner()
        Database.get_instance().new_sheet(username, sheet_name, permission)

        print(f"Create a sheet {sheet_name} for user {username}.")
        return 


class CheckSheet(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Check a sheet"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """input user name and sheet name to check a sheet"""


    def execute(self, args: tuple) -> Any:
        print("please enter: 'user_name sheet_name' ", end='\n>')
        username, sheet_name = input().split(' ')
        sheet = Database.get_instance().check_sheet(username, sheet_name)
        print(str(sheet))
        return sheet



class EditSheetValue(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Edit a sheet"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """input user name and sheet name to edit a sheet"""


    def execute(self, args: tuple) -> Any:
        print("please enter: 'user_name sheet_name' ", end='\n>')
        username, sheet_name = input().split(' ')

        db = Database.get_instance()
        sheet = db.check_sheet(username, sheet_name)
        print(str(sheet))

        print("please input (row, col, val)", end='\n>')
        row, col, val = input().split(' ')
        row = int(row)
        col = int(col)
        val = less_dangerous_eval(val)

        sheet.edit_sheet(row, col, val)
        db.update_sheet(username, sheet_name, sheet)
        print(f"Edit sheet {sheet_name} success")
        return None


class EditPermission(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Edit a sheet's access right"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """"""


    def execute(self, args: tuple) -> Any:
        print("please enter: 'user_name sheet_name (ReadOnly/Editable)' ", end='\n>')
        username, sheet_name, per_str = input().split(' ')

        match per_str:
            case 'ReadOnly':
                permission = PermissionFactory.readonly()
            case 'Editable':
                permission = PermissionFactory.editable()
            case _:
                raise ValueError("Input can only be `ReadOnly` or `Editable`")
            
        db = Database.get_instance()
        user = db.get_user_by_name(username)
        sheet = db.get_sheet_by_name(sheet_name)
        db.edit_permission(user, sheet, permission)
        print(f"user{username} to sheet{sheet_name} is set to {permission}")
        return


class ShareToUser(Command):
    # TODO: can someone override the permission that already exist??

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Collaborate with an other user."""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """enter the user name, sheet name and target user name"""


    def execute(self, args: tuple) -> Any:
        print("please enter: 'user_name sheet_name target_user' ", end='\n>')
        username, sheet_name, target_name = input().split(' ')
            
        db = Database.get_instance()
        user = db.get_user_by_name(username)
        target = db.get_user_by_name(target_name)
        sheet = db.get_sheet_by_name(sheet_name)
        permission = db.get_permission(user, sheet)
        shared_permission = permission.max_share()

        db.edit_permission(target, sheet, shared_permission)
        print(f"share sheet {sheet_name} from user {username} to {target_name}")
        return


class ExitMenuException(Exception):
    pass

class ExitMenu(Command):

    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return """Exit Menu"""

    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return """Exit Menu uwu"""


    def execute(self, args: tuple) -> Any:
        raise ExitMenuException()