import argparse
import importlib
import os

from git_qa.config_parser import ConfigParser


def valid_cmd(cmd):
    if cmd not in ["init", "run"]:
        raise argparse.ArgumentTypeError(f"({cmd}) is not a valid command")
    return cmd


def main(argv=None):
    arg_parser = argparse.ArgumentParser(description="git_qa")
    arg_parser.add_argument("-v", "--version", action="version", version="git_qa 0.0.1")  # TODO: dynamic version
    arg_parser.add_argument("cmd", help="Command", type=valid_cmd, nargs="?", default=None)
    args, pass_through_cla = arg_parser.parse_known_args(argv)

    if args.cmd is None:
        arg_parser.print_help()
        return 0

    cmd_module = importlib.import_module(f"git_qa.cmd.{args.cmd}.__main__")
    cmd_module.main(pass_through_cla)

    # arg_parser.add_argument("path", help="Root git repository directory", type=valid_path)

    # find .git folder os

    # arg_parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
    # arg_parser.add_argument("-q", "--quiet", action="store_true", help="quiet mode")
    # arg_parser.add_argument("-f", "--force", action="store_true", help="force mode")
    # arg_parser.add_argument("-c", "--config", action="store", help="config file")
    # arg_parser.add_argument("path", nargs="+", help="Path of a file or a folder of files.", type=valid_path)
    print(args)

    # config_parser = ConfigParser(file_path=args.path)

    return 0
