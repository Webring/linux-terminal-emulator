import argparse
import re
import sys

from cmd2 import CommandSet, with_argparser

def grep(filename, pattern, show_line_numbers=False, max_count=None):
    try:
        with open(filename, 'r') as file:
            count = 0
            for line_number, line in enumerate(file, start=1):
                if max_count is not None and count >= max_count:
                    break
                if re.search(pattern, line):
                    if show_line_numbers:
                        print(f"{count + 1}: {line.strip()}")
                    else:
                        print(line.strip())
                    count += 1
    except FileNotFoundError:
        print(f"grep: {filename}: No such file or directory", file=sys.stderr)

class GrepCommand(CommandSet):
    parser = argparse.ArgumentParser(description="Search for patterns in files.")
    parser.add_argument('pattern', type=str, help="Pattern to search for")
    parser.add_argument('filename', type=str, help="File to search in")
    parser.add_argument('-n', action='store_true', help="Show line numbers")
    parser.add_argument('-m', type=int, metavar='NUM', help="Stop after NUM matches")

    @with_argparser(parser)
    def do_grep(self, args):
        return self.execute(args)

    def execute(self, args):
        grep(args.filename, args.pattern, args.n, args.m)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = GrepCommand()
    command.execute_like_main()
