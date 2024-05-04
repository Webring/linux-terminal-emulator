import cmd2

import commands


class LinuxTerminalEmulator(cmd2.Cmd):
    prompt = 'linux-terminal-emulator> '

    def __init__(self):
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_ipy
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shell

        super().__init__()

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
        self.aliases.update({'source ': 'run_script'})


if __name__ == '__main__':
    app = LinuxTerminalEmulator()
    app.cmdloop()
