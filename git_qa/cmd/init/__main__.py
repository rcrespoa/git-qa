import argparse
import os

from git_qa.config_parser import ConfigParser
from git_qa.repo_installer import RepoInstaller

from .git_qa_installer import GitQAInstaller


def valid_path(path):
    # check if .git folder exists
    git_path = os.path.join(path, ".git")
    if not os.path.exists(git_path) or not os.path.isdir(git_path):
        raise argparse.ArgumentTypeError(f"({path}) git repository not found in provided path")

    # check if .git-qa-config.yaml exists
    config_path = os.path.join(path, ".git-qa-config.yaml")
    if not os.path.exists(config_path) or not os.path.isfile(config_path):
        raise argparse.ArgumentTypeError(f"({path}) .git-qa-config.yaml config file not found in provided path")

    return path


def main(argv=None) -> int:
    arg_parser = argparse.ArgumentParser(description="git_qa")
    arg_parser.add_argument("path", help="Root git repository directory", type=valid_path)
    args = arg_parser.parse_args(argv)

    # Parse config file
    config_path = os.path.join(args.path, ".git-qa-config.yaml")
    config_parser = ConfigParser(file_path=config_path)
    config = config_parser.load()

    # Install dependencies if not already installed
    remote_deps = config.get_remote_dependencies()
    repo_installer = RepoInstaller(install_path=os.path.join(args.path, ".git_qa"), remote_deps=remote_deps)
    repo_installer.install()

    # # Get reference to local hooks
    # local_ref = config.get_local_hooks_ref()

    # TODO: install local hook dependencies (i.e. isort)

    # # Merge references
    # hooks_ref = {**remote_hooks_ref, **local_ref}

    # Get event to hook mapping
    event_to_hook = config.get_event_to_hook()

    git_qa_installer = GitQAInstaller(git_path=os.path.join(args.path, ".git"), config_path=config_parser.full_path, event_to_hook=event_to_hook)
    git_qa_installer.install()
    # print(hooks_ref, event_to_hook)

    # Fetch dependencies if required

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
