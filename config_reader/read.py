import os
import platform
import stat
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

env = Path(find_dotenv('project.env'))

assert load_dotenv(env), 'No project.env found'

project_root = Path(
    env.parent
)


def get_config(node_path: str, *, conf_string_delimiter: str = None, **kwargs):
    import jmespath as jp
    import yaml

    config_file_relative_path = Path(
        os.getenv('CONFIG_PATH')
    )

    config_file = project_root.home() / config_file_relative_path

    assert (
               not os.stat(config_file).st_mode & (stat.S_IWOTH | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)
           ) or platform.system() == 'Windows', 'Check config file permissions'

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
