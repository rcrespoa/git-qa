import itertools
import os


class Config(dict):
    def get_remote_dependencies(self):
        return list()

    def _seek_local_refs(self, ref: dict, key: str):
        if key not in self:
            return
        for repo in self[key]:
            if repo["type"] == "local" and repo["path"]:
                for hook in repo["hooks"]:
                    ref[hook["id"]] = {
                        "hook_dir": os.path.join(repo["path"], hook["id"]),
                    }

                    if "config" in hook:
                        ref[hook["id"]]["config"] = hook["config"]

                    if "path" in hook:
                        ref[hook["id"]]["path"] = hook["path"]

    def _seek_event_types(self, ref: dict, key: str):
        if key not in self:
            return
        ref[key] = list(itertools.chain.from_iterable([[hook["id"] for hook in repo["hooks"]] for repo in self[key]]))

    def get_local_hooks_ref(self):
        ref = {}
        self._seek_local_refs(ref, "pre-commit")
        self._seek_local_refs(ref, "pre-push")
        return ref

    def get_event_to_hook(self, event_type: str = None):
        ref = {}
        if event_type is not None:
            self._seek_event_types(ref, event_type)
            return ref[event_type]

        self._seek_event_types(ref, "pre-commit")
        self._seek_event_types(ref, "pre-push")

        return ref
