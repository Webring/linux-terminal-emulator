import os
import argparse

from cmd2 import CommandSet, with_argparser


def create_folder(path, verbose=False):
    head, tail = os.path.split(path)

    if head and not os.path.exists(head):
        print(f"mkdir: cannot create directory ‘{path}’: No such file or directory")
        return

    if os.path.exists(path):
        print(f"mkdir: cannot create directory ‘{path}’: File exists")
        return

    os.mkdir(path)
    if verbose:
        print(f"mkdir: created directory '{path}'")


def recursive_create_folders(path, verbose=False):
    path = os.path.normpath(path)
    folders = path.split(os.path.sep)
    current_path = ""

    for folder in folders:
        current_path = os.path.join(current_path, folder)

        if not os.path.exists(current_path):
            create_folder(current_path, verbose)


class MkdirCommand(CommandSet):
    parser = argparse.ArgumentParser(description='Analog of mkdir utility with support for -p and -v flags')
    parser.add_argument('directories', metavar='DIR', nargs='+', help='Directories to create')
    parser.add_argument('-p', action='store_true', help='Create parent directories as needed')
    parser.add_argument('-v', action='store_true', help='Display a verbose output')

    @with_argparser(parser)
    def do_mkdir(self, args):
        return self.execute(args)

    def execute(self, args):
        for directory in args.directories:
            if args.p:
                recursive_create_folders(directory, verbose=args.v)
            else:
                create_folder(directory, verbose=args.v)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = MkdirCommand()
    command.execute_like_main()
