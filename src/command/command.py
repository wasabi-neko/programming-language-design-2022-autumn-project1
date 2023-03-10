from typing import Any
from abc import ABC, abstractmethod


class Command(ABC):

    def ___init__(self) -> None:
        pass

    def __str__(self) -> str:
        return 'command[' + self.brief_description() + ']'

    @abstractmethod
    def brief_description(self) -> str:
        """return a short description of this command
        Returns:
            str: a short description of the command
        """
        return ''

    @abstractmethod
    def help(self) -> str:
        """return a help message for this command
        Returns:
            str: a help string of this command
        """
        return ''


    @abstractmethod
    def execute(self, args: tuple) -> Any:
        """execute this command of tuple(arg1, arg2, ...)"""
        return None



class CommandSet():
    """A CommandSet for containing a set of command
    """
    cmds: list[Command]

    def __init__(self) -> None:
        self.cmds = []
    

    def add_cmd(self, cmd: Command):
        assert issubclass(type(cmd), Command), "The type of cmd must be Command"
        self.cmds.append(cmd)
