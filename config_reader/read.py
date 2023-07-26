def get_config(node_path: str, *, conf_string_delimiter: str = None, **kwargs):
    import jmespath as jp
    import yaml
    from pathlib import Path

    config_file = Path().home() / '.config/smai/config.yaml'

    assert config_file.exists(), 'No config file'

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
