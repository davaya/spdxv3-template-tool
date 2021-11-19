"""
Validate serialized SPDXv3 files against schema
"""
import jadn
import json
import os
import re
from urllib.parse import urlparse, urlunparse

SCHEMA = 'Schemas/spdx-v3.jidl'
DATA_DIR = 'Data3'
OUT_DIR = 'Out'


def make_iri(eid: str, cx: dict) -> str:
    u = urlparse(eid)
    if scheme := u.scheme:
        if prefix := cx.get('prefixes', {}):
            u.scheme = cx['prefixes'][prefix]
            return urlunparse(u)
    return urlunparse(u)

    print(eid, u)


def split_collection(e: dict, outfile) -> None:
    cx = e.pop('context')
    oe = {'id': make_iri(e['id'], cx), 'type': e['type']}


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
        split_collection(d, os.path.join(OUT_DIR, f))
