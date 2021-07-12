import os
import pathlib

import yaml


def load_config(root=os.getcwd()):
    with open(str(pathlib.Path(root) / 'config' / 'config.yaml')) as f:
        return yaml.safe_load(f.read())
