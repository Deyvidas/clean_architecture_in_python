from pathlib import Path as __Path

import yaml as __yaml


CONFIG_FILE_PATH = __Path(__file__).parent / 'config.yaml'


with open(CONFIG_FILE_PATH) as file:
    config_dict = __yaml.load(file, __yaml.loader.FullLoader)


__all__ = [
    'config_dict',
    'CONFIG_FILE_PATH',
]
