import ctypes
import os
import platform

import cmd2

import commands


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


class LinuxTerminalEmulator(cmd2.Cmd):
    prompt = 'linux-terminal-emulator> '

    def __init__(self):
        super().__init__()

        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_ipy
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shell

        self.default_error = "{}: command not found"

        self.hidden_commands.append('macro')
        self.hidden_commands.append('shortcuts')
        self.hidden_commands.append('run_script')
        self.hidden_commands.append('history')
        self.hidden_commands.append('help')
        self.hidden_commands.append('macro')
        self.hidden_commands.append('set')
        self.hidden_commands.append('alias')
        self.hidden_commands.append('quit')

        self.aliases.update({'ll': 'ls -l'})
        self.aliases.update({'la': 'ls -a'})
        self.aliases.update({'exit': 'quit'})
        self.aliases.update({'source': 'run_script'})

        user_permissions_symbol = "#" if is_admin() else "$"
        self.prompt = f"{os.getlogin()}@{platform.node()}{user_permissions_symbol} "


if __name__ == '__main__':
    app = LinuxTerminalEmulator()
    app.cmdloop()
