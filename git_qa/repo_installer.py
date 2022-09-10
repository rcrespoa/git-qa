import os


class RepoInstaller:
    def __init__(self, install_path: str, remote_deps: list):
        self.install_path = install_path
        self.remote_deps = remote_deps

        # Create install_path if it doens't exist
        if not os.path.exists(install_path):
            os.makedirs(install_path)

    def install(self):
        # TODO: implement install if not already installed

        # TODO: save reference to hooks, id -> path
        return dict()
