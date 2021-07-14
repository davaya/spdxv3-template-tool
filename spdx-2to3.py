"""
Translate SPDX v2.2 JSON files to SPDX v3
"""
import os
import shutil
import jadn
import json
from typing import NoReturn

SPDX_V2_SCHEMA = 'spdx-v2_2.jidl'
SPDX_V3_SCHEMA = 'spdx3-map.jidl'
DATA_DIR = 'Data'


def load_schema(filename: str) -> dict:
    fn, ext = os.path.splitext(filename)
    try:
        loader = {
            '.jadn': jadn.load,
            '.jidl': jadn.convert.jidl_load,
            '.html': jadn.convert.html_load
        }[ext]
    except KeyError:
        print(f'Unsupported schema format: {filename}')
        return {}

    print(f'{filename:}:')
    schema = loader(os.path.join('../Source', filename))
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]) + '\n')
    return schema


def translate(fn: str, out: str) -> NoReturn:
    print(f'Translate {fn}')
    codec_v2 = jadn.codec.Codec(spdxv2, verbose_rec=True, verbose_str=True)
    d2 = json.load(open(os.path.join(DATA_DIR, fn), 'r'))
    v2z = codec_v2.decode('Document', d2)


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    spdxv2 = load_schema(SPDX_V2_SCHEMA)
    spdxv3 = load_schema(SPDX_V3_SCHEMA)
    output_dir = os.path.join(DATA_DIR, '../Out')
    for f in os.listdir(DATA_DIR):
        if os.path.splitext(f)[1] == '.json':
            translate(f, output_dir)
