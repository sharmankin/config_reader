import os
import platform
import re
from pathlib import Path

from dotenv import load_dotenv, find_dotenv, set_key

env = Path(find_dotenv('project.env'))

assert load_dotenv(env), 'No project.env found'

project_root = Path(
    env.parent
)

project_in_path = False

if python_path := os.getenv('PYTHONPATH'):

    path_options = [
        project_root.as_posix()
    ]

    if platform.system() == 'Windows':
        dl, *parts = project_root.parts
        path_options += [dl.replace('\\', r'\\') + r'\\'.join(parts)]

    path_pattern = '(?:' + '|'.join(path_options) + ')'

    project_in_path = bool(
        re.search(r'(?<=[:;])|(?<=^)' + path_pattern + r'(?=;|:|$)', python_path)
    )

if not project_in_path:
    set_key(env, 'PYTHONPATH', project_root.as_posix(), quote_mode='auto', export=True)
    load_dotenv(env)


def get_config(node_path: str, *, conf_string_delimiter: str = None, **kwargs):
    import jmespath as jp
    import yaml

    config_file_relative_path = Path(
        os.getenv('CONFIG_PATH')
    )

    config_file = project_root.home() / config_file_relative_path

    assert config_file.exists(), f'No config file {config_file.absolute().as_posix()}'

    if isinstance(config := jp.search(
            node_path,
            yaml.full_load(
                config_file.read_bytes(),
            )
    ), dict):
        config = config | kwargs

    assert config, f'No config found for {node_path}'

    if conf_string_delimiter is None or not isinstance(config, dict):
        return config

    return str(conf_string_delimiter).join(f'{k}={v}' for k, v in config.items())
