import argparse
import os
from pathlib import Path
from typing import Optional

import dotenv


def main(parent_parser: Optional[argparse.ArgumentParser] = None):
    lib_conf = Path(__file__).parent.parent / 'config_reader/lib.env'

    default_root = Path('.').absolute()

    ap = argparse.ArgumentParser(
        prog='Config Reader',
        parents=list(filter(bool, [parent_parser]))
    )

    ap.add_argument(
        '--project-root', '-r',
        help='Project root directory',
        default=default_root.as_posix(),
        type=Path,
        metavar=''
    )

    ap.add_argument(
        '--config', '-c',
        help='Path to config.yaml',
        required=True,
        type=Path,
        metavar=''
    )

    ap.add_argument(
        '--force',
        action='store_true',
        help='Rebuild configuration'
    )

    ap.add_argument(
        '--env', '-e',
        action='append',
        type=str,
        help='Set additional variables for dotevn as -e "KEY=VALUE"',
        metavar=''
    )

    args = ap.parse_args()

    pc: Path

    if not lib_conf.exists() or args.force:
        dotenv.set_key(
            lib_conf,
            'PROJECT_ROOT',
            args.project_root.as_posix(),
            export=True
        )
        dotenv.set_key(
            lib_conf,
            'CONFIG_PATH',
            args.config.as_posix(),
            export=True
        )

        dotenv.set_key(
            lib_conf,
            'PYTHONPATH',
            args.project_root.as_posix()
        )

        dotenv.set_key(
            lib_conf,
            'VIRTUAL_ENV',
            os.getenv('VIRTUAL_ENV')
        )

        for item in args.env:
            key, value = item.split('=')
            dotenv.set_key(
                lib_conf,
                key,
                value
            )

        Path(args.project_root / 'project.env').symlink_to(
            lib_conf
        )
