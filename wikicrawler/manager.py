# -*- coding: utf-8 -*-

import sys

from cmds.database import init_db, reset_db


def help_fn():
    print("/--------------------------------------------\\")
    print("Commands list:")
    print()
    print("- \'init\' - init database for crawlers")
    print("- \'reset\' - reset database for crawlers")
    print("\\--------------------------------------------/")


def exec_cmd(args):
    func = {
        'help': help_fn,

        'init': init_db,
        'reset': reset_db,
    }

    cmd = args[1]

    if cmd not in func.keys():
        raise Exception("Unknown command! Print \"%s\"" % 'help')

    func.get(cmd)()


if __name__ == "__main__":
    exec_cmd(sys.argv)
