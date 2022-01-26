"""
Translate SPDX v2.2 JSON files to SPDX v3
"""

import jadn
import json
import os
import re
from datetime import datetime, timezone

SPDX_V2_SCHEMA = 'spdx-v2_2.jidl'
SPDX_V3_SCHEMA = 'spdx-v3.jidl'
DATA_DIR = 'Data2'
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
    fname, ext = os.path.splitext(filename)
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


def translate_2to3(v2doc: dict, verbose_id=False) -> dict:
    element = {
        'id': v2doc['SPDXID'],      # Get actual ID of SBOM Element.  (not SPDXRef-DOCUMENT)
        'type': {
            'sbom': {}
        },
        'name': v2doc.get('name', ''),      # Do not populate if empty
        'summary': v2doc.get('summary', ''),
        'description': v2doc.get('description', ''),
        'comment': v2doc.get('comment', ''),
        # verifiedUsing
        # 'externalReferences': v2doc['externalDocumentRefs']
        # 'extension': no spdx2 equivalent
        # creationInfo comment: no spdx3 equivalent
    }
    document_context = {
        'specVersion': v2doc['spdxVersion'],
        'created': {
            'by': v2doc['creationInfo']['creators'],
            'when': int2datems(datems2int(v2doc['creationInfo']['created'])),   # Serialize epoch or string?
        },
        'profiles': ['Core'],
        'dataLicense': v2doc['dataLicense'],
        'namespace': v2doc['documentNamespace']
    }
    artifacts, identities, relationships, annotations = [], [], [], []      # Add elementValues and elementRefs to document_context

    element.update({'context': document_context})       # Use pseudo-property serialization
    # return [element, document_context]                # use ContextElement serialization
    return element


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    codec2 = jadn.codec.Codec(load_schema(SPDX_V2_SCHEMA), verbose_rec=True, verbose_str=True)
    codec3 = jadn.codec.Codec(load_schema(SPDX_V3_SCHEMA), verbose_rec=True, verbose_str=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fx in os.listdir(DATA_DIR):
        fn, ext = os.path.splitext(fx)
        if ext == '.json':
            print(f'{fx}:')
            d2 = json.load(open(os.path.join(DATA_DIR, fx), 'r'))
            doc2 = codec2.decode('Document', d2)
            doc3 = translate_2to3(doc2)
            d3 = codec3.encode('Element', doc3)
            with open(os.path.join(OUTPUT_DIR, fn + '_v3.json'), 'w') as fo:
                json.dump(d3, fo, indent=2)
