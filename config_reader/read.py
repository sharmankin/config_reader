import os
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
