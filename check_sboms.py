"""
Validate serialized SPDXv3 files against schema
"""
import jadn
import json
import os

SCHEMA = 'Schemas/spdx-v3.jidl'
DATA_DIR = 'Data3'


def load_any(path: str) -> (dict, None):
    fn, ext = os.path.splitext(path)
    try:
        loader = {
            '.jadn': jadn.load,
            '.jidl': jadn.convert.jidl_load,
            '.html': jadn.convert.html_load
        }[ext]
    except KeyError:
        if os.path.isfile(path):
            raise ValueError(f'Unsupported schema format: {path}')
        return
    return loader(path)


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    s = load_any(SCHEMA)
    sc = jadn.codec.Codec(s, verbose_rec=True, verbose_str=True)
    for f in os.listdir(DATA_DIR):
        print(f)
        data = json.load(open(os.path.join(DATA_DIR, f)))
        d = sc.decode('Element', data)
