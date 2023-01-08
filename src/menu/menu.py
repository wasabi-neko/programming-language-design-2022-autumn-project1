import sys
import traceback

from command.command import Command, CommandSet
import menu.menu_cmds as menu_cmds
from exceptions.exceptions import AppException, ExitMenuException, ArgError


def print_exception_info(e: Exception):
    print(str(e.__traceback__))
    error_class = e.__class__.__name__ 
    detail = e.args[0] 
    cl, exc, tb = sys.exc_info() 
    lastCallStack = traceback.extract_tb(tb)[-1]
    fileName = lastCallStack[0]
    lineNum = lastCallStack[1]
    funcName = lastCallStack[2]
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)


class Menu(CommandSet):
    no_prompt: bool
    debug: bool

    def __init__(self, no_prompt=False, debug=False) -> None:
        super().__init__()
        self.no_prompt = no_prompt
        self.debug = debug

        self.add_cmd(menu_cmds.CreateUser())
        self.add_cmd(menu_cmds.CreateSheet())
        self.add_cmd(menu_cmds.CheckSheet())
        self.add_cmd(menu_cmds.EditSheetValue())
        self.add_cmd(menu_cmds.EditPermission())
        self.add_cmd(menu_cmds.ShareToUser())
        self.add_cmd(menu_cmds.ExitMenu())
    

    def content_border(self, content: list[str], title: str, border: str) -> str:
        max_len = len(max(content, key=len))
        result = '\n'
        result += border * int((max_len - len(title)) / 2)
        result += title
        result += border * int((max_len - len(title)) / 2) + '\n'
        result += ''.join(content)
        result += border * max_len
        return result
    

    def print_all_cmd(self) -> None:
        cmd_strs = []
        for i, cmd in enumerate(self.cmds):
            cmd_strs.append(f"{i+1}. {cmd.brief_description()}\n")
        
        print_str = self.content_border(cmd_strs, 'Menu', '-')
        print(print_str)


    def print_help(self) -> None:
        cmd_strs = []
        for i, cmd in enumerate(self.cmds):
            cmd_strs.append(f"{i+1}. {cmd.help()}\n")
        
        print_str = self.content_border(cmd_strs, 'HELP', '-')
        print(print_str)
    

    def read_cmd_num(self) -> int:
        str_in = input('>')
        if not str_in.isnumeric():
            raise  ArgError('please input a number')
        return int(str_in)
        

    def menu_loop(self) -> None:
        continue_loop = True
        while(continue_loop):
            # prompt
            if not self.no_prompt:
                self.print_all_cmd()

            # command
            try:
                num = self.read_cmd_num()
                # execute selected command
                self.cmds[num - 1].execute(())

            except (EOFError, ExitMenuException) as e:
                continue_loop = False
                continue

            except (AppException) as e:
                print('Error: ', e)

            except Exception as e:
                if self.debug:
                    print_exception_info(e)
        # End menu loop----------------------------------------
        print("bye")
    