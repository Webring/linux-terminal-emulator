import argparse
import os

from cmd2 import CommandSet, with_argparser


def get_current_directory(follow_symlinks=False):
    if follow_symlinks:
        return os.getcwd()
    else:
        return os.path.realpath(os.getcwd())


class PwdCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Print the name of the current working directory.")
    parser.add_argument('-L',
                        action='store_true',
                        help="print the value of $PWD if it names the current working directory")
    parser.add_argument('-P',
                        action='store_true',
                        help="print the physical directory, without any symbolic links")

    @with_argparser(parser)
    def do_pwd(self, args):
        return self.execute(args)

    def execute(self, args):
        if args.L and args.P:
            print("Options -L and -P are mutually exclusive.")
            return

        if args.P:
            print(get_current_directory())
        elif args.L:
            print(os.environ.get('PWD', get_current_directory()))
        else:
            print(get_current_directory(follow_symlinks=True))

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = PwdCommand()
    command.execute_like_main()
