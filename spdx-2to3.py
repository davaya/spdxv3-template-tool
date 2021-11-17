"""
Translate SPDX v2.2 JSON files to SPDX v3
"""

import jadn
import json
import os
import re
from datetime import datetime, timezone
from typing import NoReturn

SPDX_V2_SCHEMA = 'spdx-v2_2.jidl'
SPDX_V3_SCHEMA = 'spdx-v3.jidl'
DATA_DIR = 'Data'
SCHEMA_DIR = 'Schemas'
OUTPUT_DIR = 'Out'


def int2datems(dt: int) -> str:
    y = datetime.isoformat(datetime.fromtimestamp(dt/1000., timezone.utc))
    if m := re.match(r'^(.+)(\.\d\d\d)(\d\d\d)(.+)$', y):   # strip microseconds to milliseconds
        y = m.group(1) + m.group(2) + m.group(4)
    return y


def datems2int(dts: str) -> int:
    x = datetime.fromisoformat(dts.upper().replace('Z', '+00:00').replace(' ', 'T'))
    return int(1000 * datetime.timestamp(x))


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
    schema = loader(os.path.join(SCHEMA_DIR, filename))
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]) + '\n')
    return schema


def translate_2to3(v2doc: dict, verbose_id=False) -> list:
    document = {
        'element': {
            'id': v2doc['SPDXID'],
            'createdWhen': datems2int(v2doc['creationInfo']['created']),
            'createdBy': v2doc['creationInfo']['creators'],
            # 'verifiedUsing': no spdx2 equivalent
            'externalReferences': v2doc['externalDocumentRefs'],
            'name': v2doc.get('name', None),
            'summary': v2doc.get('summary', None),
            'description': v2doc.get('description', None),
            'comment': v2doc.get('comment', None),
            # creationInfo comment: no spdx3 equivalent
            # 'extension': no spdx2 equivalent
        },
        'namespace': v2doc['documentNamespace'],
        'specVersion': v2doc['spdxVersion'],
        'profiles': 'Core',      # Profile Identifiers?
        'dataLicense': v2doc['dataLicense']
    }
    v3sbom = [{'document': document}]
    artifacts, identities, relationships, annotations = [], [], [], []
    v3sbom += artifacts
    v3sbom += identities
    v3sbom += relationships
    v3sbom += annotations
    if not verbose_id:
        for n, e in v3sbom:
            e['element']['id'] = n
    return v3sbom


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    codec2 = jadn.codec.Codec(load_schema(SPDX_V2_SCHEMA), verbose_rec=True, verbose_str=True)
    codec3 = jadn.codec.Codec(load_schema(SPDX_V3_SCHEMA), verbose_rec=True, verbose_str=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fn in os.listdir(DATA_DIR):
        if os.path.splitext(fn)[1] == '.json':
            d2 = json.load(open(os.path.join(DATA_DIR, fn), 'r'))
            doc2 = codec2.decode('Document', d2)
            doc3 = translate_2to3(doc2, verbose_id=True)
            d3 = codec3.encode('SpdxDocument', doc3)
            with open(os.path.join(OUTPUT_DIR, fn), 'w') as fo:
                json.dump(d3, fo)
