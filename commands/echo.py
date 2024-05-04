import argparse

from cmd2 import CommandSet, with_argparser


class EchoCommand(CommandSet):
    parser = argparse.ArgumentParser(description='An echo-like utility')
    parser.add_argument('text', nargs='*', help='Text to be echoed')
    parser.add_argument('-n', action='store_true', help='Do not output the trailing newline')
    parser.add_argument('-e', action='store_true', help='Enable interpretation of backslash escapes')

    @with_argparser(parser)
    def do_echo(self, args):
        return self.execute(args)

    def execute(self, args):
        text = ' '.join(args.text)
        if args.e:
            text = bytes(text, 'utf-8').decode('unicode_escape')
        end = '' if args.n else '\n'
        print(text, end=end, flush=True)

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == '__main__':
    command = EchoCommand()
    command.execute_like_main()
