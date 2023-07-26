import inspect
import os
from pathlib import Path

project_root = Path(os.path.commonpath((inspect.stack()[0].filename, inspect.stack()[1].filename)))


def get_config(node_path: str, *, conf_string_delimiter: str = None, **kwargs):
    import jmespath as jp
    import yaml

    project_name = kwargs.get('project_name', project_root.name.lower())

    config_file = project_root.home() / f'.config/{project_name}/config.yaml'

    assert config_file.exists(), 'No config file'

    i = inspect.stack()

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
