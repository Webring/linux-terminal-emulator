import os
import argparse
import shutil

from cmd2 import CommandSet, with_argparser


class MvCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Rename source to DEST, or move source(s) to DIRECTORY.")
    parser.add_argument("source",
                        help="source file or directory to move.")
    parser.add_argument("destination",
                        help="destination directory to move the source file or directory to.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite the destination directory or file if it already exists.")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output.")

    @with_argparser(parser)
    def do_mv(self, args):
        return self.execute(args)

    def execute(self, args):
        if not os.path.exists(args.source):
            print(f"Error: source file or directory '{args.source}' does not exist.")
            return

        if os.path.isdir(args.destination) and not os.path.exists(args.destination):
            print(f"Error: destination directory '{args.destination}' does not exist.")
            return

        if os.path.isdir(args.source):
            if os.path.exists(args.destination):
                if not args.force:
                    print(f"Error: Directory '{args.destination}' already exists. Use the -f flag to overwrite.")
                    return
                else:
                    if args.verbose:
                        print(f"Overwriting directory '{args.destination}'...")
                    shutil.rmtree(args.destination)

            if args.verbose:
                print(f"Moving directory '{args.source}' to '{args.destination}'...")
            shutil.move(args.source, args.destination)
        else:
            if os.path.isdir(args.destination):
                args.destination = os.path.join(args.destination, os.path.basename(args.source))

            if os.path.exists(args.destination):
                if not args.force:
                    print(f"Error: File '{args.destination}' already exists. Use the -f flag to overwrite.")
                    return
                else:
                    if args.verbose:
                        print(f"Overwriting file '{args.destination}'...")
                    os.remove(args.destination)

            if args.verbose:
                print(f"Moving file '{args.source}' to '{args.destination}'...")
            shutil.move(args.source, args.destination)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = MvCommand()
    command.execute_like_main()
