import sys
import traceback

from command.command import Command, CommandSet
import menu.menu_cmds as menu_cmds
from exceptions.exceptions import AppException, ExitMenuException


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
    

    def print_all_cmd(self) -> None:
        cmd_str = ''
        max_cmd_len = 0

        for i, cmd in enumerate(self.cmds):
            line = f"{i+1}. "
            line += cmd.brief_description()
            max_cmd_len = len(line) if len(line) > max_cmd_len else max_cmd_len
            cmd_str += line + '\n'
        
        name = 'menu'
        print_str = '\n'
        print_str += "-" * int((max_cmd_len - len(name)) / 2)
        print_str += name
        print_str += "-" * int((max_cmd_len - len(name)) / 2)
        print_str += '\n'
        print_str += cmd_str
        print_str += '-' * max_cmd_len
        print(print_str)


    def print_help(self) -> None:
        # TODO: length of prompt 
        print('---help--')
        for i, cmd in enumerate(self.cmds):
            print(f"{i+1}. ", end='')
            print(cmd.help())
        print('---')


    def menu_loop(self) -> None:
        while(True):
            # prompt
            if not self.no_prompt:
                self.print_all_cmd()

            # command
            try:
                str_in = input('>')
                num = 0
                if str_in.isnumeric():
                    num = int(str_in)
                else:
                    print('please input a number')
                    break

                # execute selected command
                self.cmds[num - 1].execute(())

            except (EOFError, ExitMenuException) as e:
                break
            except (AppException) as e:
                print('Error: ', e)
            except Exception as e:
                print(e)
                if self.debug:
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
        
        print("bye")
    