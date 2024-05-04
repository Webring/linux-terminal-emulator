import argparse
import os
import shutil

from cmd2 import CommandSet, with_argparser


def copy(src, dst, recursive=False, verbose=False):
    try:
        if os.path.isdir(src):
            if not recursive:
                raise NotADirectoryError(f"'{src}' is a directory (not copied).")
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        if verbose:
            print(f"'{src}' -> '{dst}'")
    except FileNotFoundError:
        print(f"cp: cannot stat '{src}': No such file or directory")
    except PermissionError:
        print(f"cp: cannot open '{src}' for reading: Permission denied")
    except NotADirectoryError as e:
        print(f"cp: cannot copy '{src}': {e}")
    except shutil.SameFileError:
        print(f"cp: '{src}' and '{dst}' are the same file")


class CpCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Copy files and directories.")
    parser.add_argument("source", help="source file or directory")
    parser.add_argument("destination", help="destination file or directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="copy directories recursively")
    parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")

    @with_argparser(parser)
    def do_cp(self, args):
        return self.execute(args)

    def execute(self, args):
        copy(args.source, args.destination, args.recursive, args.verbose)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = CpCommand()
    command.execute_like_main()
