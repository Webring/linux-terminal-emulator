import os
import argparse
import time
import stat

import win32security
from cmd2 import CommandSet, with_argparser


def get_file_owner(file_path):
    try:
        info = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = info.GetSecurityDescriptorOwner()
        owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return owner_name
    except Exception as e:
        print("Ошибка при получении владельца файла:", e)
        return None


def get_file_group(file_path):
    try:
        info = win32security.GetFileSecurity(file_path, win32security.GROUP_SECURITY_INFORMATION)
        group_sid = info.GetSecurityDescriptorGroup()
        group_name, _, _ = win32security.LookupAccountSid(None, group_sid)
        return group_name
    except Exception as e:
        print("Ошибка при получении группы пользователя файла:", e)
        return None


class LsCommand(CommandSet):
    parser = argparse.ArgumentParser(description="List information about the FILEs (the current directory by default).")
    parser.add_argument("path", nargs="?", default=".", help="Path to directory (default: current directory)")
    parser.add_argument("-a", "--all", action="store_true", help="do not ignore entries starting with .")
    parser.add_argument("-l", "--long", action="store_true", help="Use a long listing format")

    @with_argparser(parser)
    def do_ls(self, args):
        return self.execute(args)

    def execute(self, args):
        if not os.path.isdir(args.path):
            print(f"ls: cannot access '{args.path}': No such file or directory")
            return

        files = os.listdir(args.path)
        if not args.all:
            files = [f for f in files if not f.startswith('.')]

        if not args.long:
            print(*files, sep=' ')
            return

        print(f"total {len(files)}")
        for f in files:
            file_path = os.path.join(args.path, f)
            file_stat = os.stat(file_path)
            mode = stat.filemode(file_stat.st_mode)
            size = file_stat.st_size
            owner = get_file_owner(file_path)
            owner_group = get_file_group(file_path)
            last_modified = time.strftime("%b %d %H:%M", time.localtime(file_stat.st_mtime))
            print(f"{mode:10} {owner}  {owner_group} {size:10} {last_modified} {'':10} {f}")

    def execute_like_main(self):
        args = self.parser.parse_args()
        self.execute(args)


if __name__ == "__main__":
    command = LsCommand()
    command.execute_like_main()
