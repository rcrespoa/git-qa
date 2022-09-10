import io
import os
from typing import List


class GitQAInstaller:
    def __init__(self, git_path: str, config_path: dict, event_to_hook: dict):
        self.git_path = git_path
        self.config_path = config_path
        self.event_to_hook = event_to_hook

    def _handle_event(self, event_type: str, hook_ids: List[str]):
        with io.StringIO() as f:
            f.write("#!/bin/bash\n")
            # f.write("git_qa validate\n") # TODO: validate config file is synced
            f.write(f"git-qa run --event {event_type} {os.path.dirname(self.config_path)}\n")

            print(f.getvalue())

    def install(self):
        for event_type, hook_ids in self.event_to_hook.items():
            self._handle_event(event_type, hook_ids)

        # Load current file

        # Generate file and compare with existing file

        # if file is different, update file
