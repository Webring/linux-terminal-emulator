import argparse
import os

from cmd2 import CommandSet, with_argparser


class CatCommand(CommandSet):
    parser = argparse.ArgumentParser(description='Concatenate FILE(s) to standard output.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+', help='Files to display')
    parser.add_argument('-n', "--number", action='store_true', help='number all output lines')
    parser.add_argument('-E', "--show-ends", action='store_true', help='display $ at end of each line')

    @with_argparser(parser)
    def do_cat(self, args):
        return self.execute(args)

    def execute(self, args):
        total_lines = 0
        for filename in args.files:
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
                break

            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    total_lines += 1
                    if args.number:
                        print(f"{total_lines}: ", end="")
                    print(line.rstrip(), end="")
                    if args.show_ends:
                        print("$", end="")
                    print()

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == "__main__":
    command = CatCommand()
    command.execute_like_main()
