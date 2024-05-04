import os
import argparse

from cmd2 import CommandSet, with_argparser


def change_directory(path, logical=True):
    try:
        if logical:
            os.chdir(path)
        else:
            os.chdir(os.path.realpath(path))
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")


class CdCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Change the current working directory.")
    parser.add_argument("directory", nargs="?", default=".",
                        help="The directory to change to (default is the current directory)")
    parser.add_argument("-P", action="store_true",
                        help="Use the physical directory structure without following symbolic links")
    parser.add_argument("-L", action="store_true", help="Follow symbolic links (default behavior)")

    @with_argparser(parser)
    def do_cd(self, args):
        return self.execute(args)

    def execute(self, args):
        if args.P and args.L:
            self.parser.error("cannot specify both -P and -L")

        logical = not args.P if args.L else args.P
        change_directory(args.directory, logical)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = CdCommand()
    command.execute_like_main()
