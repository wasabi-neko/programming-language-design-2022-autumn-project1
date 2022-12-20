import argparse
from menu.menu import Menu


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="print debug message", action="store_true")
    parser.add_argument("--no_prompt", help="disable prompt", action="store_true")
    args = parser.parse_args()

    no_prompt = False
    debug = False

    if args.debug:
        debug = True
    if args.no_prompt:
        no_prompt = True

    menu = Menu(no_prompt, debug)
    menu.menu_loop()
