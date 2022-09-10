import argparse
import os

from git_qa.config_parser import ConfigParser
from git_qa.hook_executor import HookExecutor
from git_qa.repo_installer import RepoInstaller


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


def valid_event(event):
    if event not in ["pre-commit", "post-commit", "pre-push", "post-push"]:
        raise argparse.ArgumentTypeError(f"({event}) is not a valid event")
    return event


def main(argv=None) -> int:
    arg_parser = argparse.ArgumentParser(description="git_qa")
    arg_parser.add_argument("--event", help="Event type (GIT HOOK)", type=valid_event)
    arg_parser.add_argument("path", help="Root git repository directory", type=valid_path)
    args = arg_parser.parse_args(argv)

    config_path = os.path.join(args.path, ".git-qa-config.yaml")
    config_parser = ConfigParser(file_path=config_path)
    config = config_parser.load()

    remote_deps = config.get_remote_dependencies()
    repo_installer = RepoInstaller(install_path=os.path.join(args.path, ".git_qa"), remote_deps=remote_deps)
    remote_hooks_ref = repo_installer.install()

    # Get reference to local hooks
    local_ref = config.get_local_hooks_ref()

    # Merge references
    hooks_ref = {**remote_hooks_ref, **local_ref}

    hook_ids = config.get_event_to_hook(event_type=args.event)

    # TODO: render UI of hooks to be executed / progress

    for hook_id in hook_ids:
        HookExecutor(hook_id=hook_id, default_paths=config["default_paths"], **hooks_ref[hook_id]).execute()


if __name__ == "__main__":
    raise SystemExit(main())
