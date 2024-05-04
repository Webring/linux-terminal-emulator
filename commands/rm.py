import argparse
import os
import shutil

from cmd2 import CommandSet, with_argparser


def remove_file(file_path, force):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        if not force:
            print(f"rm: cannot remove '{file_path}': No such file or directory")
    except PermissionError:
        if not force:
            print(f"rm: cannot remove '{file_path}': Permission denied")


def remove_directory(directory_path, force):
    try:
        shutil.rmtree(directory_path)
    except FileNotFoundError:
        if not force:
            print(f"rm: cannot remove '{directory_path}': No such file or directory")
    except PermissionError:
        if not force:
            print(f"rm: cannot remove '{directory_path}': Permission denied")


class RmCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Remove files or directories.")
    parser.add_argument("files", metavar="FILE", nargs="+", help="Files or directories to remove")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Remove directories and their contents recursively")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Ignore nonexistent files and arguments, never prompt")

    @with_argparser(parser)
    def do_rm(self, args):
        return self.execute(args)

    def execute(self, args):
        for file_path in args.files:
            if os.path.isfile(file_path):
                remove_file(file_path, args.force)
            elif os.path.isdir(file_path):
                if args.recursive:
                    remove_directory(file_path, args.force)
                else:
                    if not args.force:
                        print(f"rm: cannot remove '{file_path}': Is a directory")
            else:
                if not args.force:
                    print(f"rm: cannot remove '{file_path}': No such file or directory")

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = RmCommand()
    command.execute_like_main()
