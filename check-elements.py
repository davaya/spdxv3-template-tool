"""
Expand documents containing element+context into multiple individual elements
"""
import jadn
import json
import os
from urllib.parse import urlparse

SCHEMA = 'Schemas/spdx-v3.jidl'
DATA_DIR = 'Data3'
OUT_DIR = 'Out'
DEFAULT_PROPERTIES = ('specVersion', 'created', 'profile', 'dataLicense')
IRI_LOCATIONS = ('id', 'created/by', '*/elements/*', 'relationship/from', 'relationship/to/*',
                 '*/originator', 'elementRefs/id', 'annotation/subject')


def expand_iri(context: dict, element_id: str) -> str:
    """
    Convert an Element ID in namespace:local form to an IRI
    """
    if context:
        u = urlparse(element_id)
        if u.scheme:
            if prefix := context['prefixes'].get(u.scheme, ''):
                return prefix + u.path
            return element_id
        if element_id not in context.get('doc_ids', []):
            print(f'    Undefined Element: {element_id}')
        return context.get('namespace', '') + element_id
    return element_id


def compress_iri(context: dict, iri: str) -> str:
    """
    Convert an Element ID IRI to namespace:local form
    """
    if context:
        if base := context.get('namespace', ''):
            if iri.startswith(base):
                return iri.replace(base, '')
        for k, v in context.get('prefixes', {}).items():
            if iri.startswith(v):
                return iri.replace(v, k + ':')
    return iri


def expand_ids(context: dict, element: dict, paths: list) -> None:
    """
    Convert all IRIs in an element from namespace:local form to absolute IRI

    Hardcode IRI locations for now; replace with path-driven update
    """
    element.update({'id': expand_iri(context, element['id'])})
    if 'created' in element:
        element['created']['by'] = [expand_iri(context, k) for k in element['created']['by']]
    for etype, eprops in element['type'].items():
        for p in eprops:
            if p in ('elements', 'rootElements', 'originator', 'members'):
                eprops[p] = [expand_iri(context, k) for k in eprops[p]]
        if etype == 'annotation':
            eprops['subject'] = expand_iri(context, eprops['subject'])
        elif etype == 'relationship':
            eprops['from'] = expand_iri(context, eprops['from'])
            eprops['to'] = [expand_iri(context, k) for k in eprops['to']]


def compress_ids(context: dict, element: dict) -> None:
    """
    Convert all IRIs in an element from absolute IRI to namespace:local form

    Hardcode IRI locations for now; replace with path-driven update
    """
    element.update({'id': compress_iri(context, element['id'])})
    if 'created' in element:
        element['created']['by'] = [compress_iri(context, k) for k in element['created']['by']]
    for etype, eprops in element['type'].items():
        for p in eprops:
            if p in ('elements', 'rootElements', 'originator', 'members'):
                eprops[p] = [compress_iri(context, k) for k in eprops[p]]
        if etype == 'annotation':
            eprops['subject'] = compress_iri(context, eprops['subject'])
        elif etype == 'relationship':
            eprops['from'] = compress_iri(context, eprops['from'])
            eprops['to'] = [compress_iri(context, k) for k in eprops['to']]


def expand_element(context: dict, element: dict) -> dict:
    """
    Fill in Element properties from Context
    """
    element_x = {'id': ''}      # put id first
    element_x.update({k: context[k] for k in DEFAULT_PROPERTIES if k in context})
    element_x.update(element)
    expand_ids(context, element_x, IRI_LOCATIONS)
    return element_x


def compress_element(context: dict, element_x: dict) -> dict:
    element = {k: v for k, v in element_x.items() if v != context.get(k, '')}
    compress_ids(context, element)
    return element


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


def dump_elements(context: dict, elements: list[dict]) -> None:
    print('Context:', context)
    for e in elements:
        print(compress_element(context, e))


def validate_document(document: dict) -> dict:
    cx = {k: document[k] for k in document if k not in ('elements', 'documentRefs', 'namespaceMap')}
    cx['doc_ids'] = [compress_iri(cx, e['id']) for e in document['elements']]
    cx['ref_ids'] = [ref['namespace'] + ':' + e for ref in document.get('documentRefs', []) for e in ref['elements']]
    cx['prefixes'] = {prefix: uri for uri, prefix in document.get('namespaceMap', {}).items()}
    # Check defined vs copied namespaces and timestamps
    return cx


def make_dot(context: dict, elist: list, fp: str) -> None:
    ex = {e['id']: k for k, e in enumerate(elist, start=1)}
    with open(os.path.splitext(fp)[0] + '.dot', 'w') as fx:
        fx.write('digraph G {\nnode [fontname=Arial, fontsize=8, shape=box, style=filled, fillcolor=lightskyblue1]\n')
        for e in elist:
            eid = compress_iri(context, e['id'])
            # print(f"  n{ex[e['id']]}: {eid}: {e.get('name', eid)}")
            fx.write(f"n{ex[e['id']]} [label=\"{eid}\\n{e.get('name', '')}\"]\n")
            for t in e['type']:
                for n in e['type'][t].get('elements', []):
                    dest = f'n{ex[n]}' if n in ex else f'"{compress_iri(context, n)}"'
                    fx.write(f"  n{ex[e['id']]} -> {dest}\n")
        fx.write('}\n')


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    os.makedirs(OUT_DIR, exist_ok=True)
    s = load_any(SCHEMA)
    sc = jadn.codec.Codec(s, verbose_rec=True, verbose_str=True)
    for f in os.scandir(DATA_DIR):
        if not f.is_file() or os.path.splitext(f)[1] not in ('.json'):
            continue
        print(f'  === {f.name}')
        doc = sc.decode('UnitOfTransfer', json.load(open(f.path)))
        ctx = validate_document(doc)
        x_elements = [expand_element(ctx, e) for e in doc['elements']]
        dump_elements(ctx, x_elements)
        make_dot(ctx, x_elements, os.path.join(OUT_DIR, f.name))
