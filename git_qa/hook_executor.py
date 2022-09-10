import json
import os
import subprocess
from typing import List


class HookExecutor:
    def __init__(self, hook_id: str, hook_dir: str, default_paths: List[str] = None, config=None, path=None):
        self.hook_id = hook_id
        self.hook_dir = hook_dir
        self.config = config
        self.path = path
        self.default_paths = default_paths

    def execute(self):
        # verify hook exists and is a directory
        if not os.path.isdir(self.hook_dir):
            raise RuntimeError(f"({self.hook_dir}) is not a directory")

        # verify hook has a metadata.json file
        metadata_path = os.path.join(self.hook_dir, "metadata.json")
        if not os.path.isfile(metadata_path):
            raise RuntimeError(f"({self.hook_dir}) does not have a metadata.json file")

        # load metadata.json
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        for prop in ["entrypoint", "config"]:
            if prop not in metadata:
                raise RuntimeError(f"({self.hook_id}) does not have a {prop} property")

        config_path = None
        if metadata["config"]:
            if self.config:
                config_path = self.config
            elif "default_config" in metadata:
                config_path = os.path.join(self.hook_dir, metadata["default_config"])
            else:
                raise RuntimeError(f"({self.hook_id}) requires a configuration file")

        if self.path:
            path = ",".join(self.path)
        elif self.default_paths is not None:
            path = ",".join(self.default_paths)
        else:
            raise RuntimeError(f"({self.hook_id}) requires a path")

        execution_cmd = ["bash", os.path.join(self.hook_dir, metadata["entrypoint"]), path]

        if config_path is not None:
            execution_cmd.append(config_path)

        print(execution_cmd)
        results = subprocess.run(execution_cmd)
        if results.returncode != 0:
            msg = results.stderr.decode() if results.stderr else f"[{self.hook_id}] Exit code != 0"
            raise RuntimeError(msg)
