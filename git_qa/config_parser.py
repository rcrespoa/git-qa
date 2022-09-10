import os
import pathlib
import sys
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import yaml  # type: ignore
from git_qa.config import Config
from jsonschema import validate  # type: ignore


class ConfigParser:
    """Parse and validate config file"""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.worskspace_path = str(pathlib.Path(file_path).parent.resolve())
        self.full_path = os.path.join(self.worskspace_path, ".git-qa-config.yaml")

    def _recursive_inject_path(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Inject path to config file"""
        config_copy = deepcopy(data)

        if isinstance(data, str):
            return data.replace("$WORKSPACE", self.worskspace_path)

        if isinstance(data, list):
            return [self._recursive_inject_path(item) for item in data]

        if isinstance(data, dict):
            return {key: self._recursive_inject_path(value) for key, value in data.items()}

        return config_copy

    # def _validate(self, config: dict) -> None:
    #     """Validate deploy file has expected format"""
    #     if "version" not in config:
    #         raise Exception("YAML version is not specified")

    #     if config["version"] not in SCHEMAS:
    #         raise Exception("Deploy version is not valid")

    #     validate(instance=config, schema=SCHEMAS[config["version"]])

    def load(self) -> Config:
        """Load config file"""
        try:
            with open(self.file_path, "r") as f:
                module_config = yaml.safe_load(f)
        except Exception as err:
            print(f"Invalid YAML file. {str(err)}")
            sys.exit(1)

        module_config = self._recursive_inject_path(module_config)
        # self._validate(module_config) # TODO: validate config file

        return Config(**module_config)
