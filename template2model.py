import jadn
import os
import re
from collections import defaultdict

"""
Generate serializations from an SPDX v3 template using a JADN information model
"""

DATA_DIR = 'Templates'
OUTPUT_DIR = 'Out'
TEMPLATE_ROOT_DIR = os.path.join('..', 'spec-v3-template', 'model')
TEMPLATE_ROOT_REPO = 'https://api.github.com/repos/spdx/spec-v3-template/contents/model'
TEMPLATE_FILE = 'SpdxV3 Core Namespace Template.md'
OUTPUT_FILE = 'spdxv3-from-list-template'
MODEL_DIRS = ('Classes', 'Properties', 'Vocabularies')


def list_dir(dirname: str) -> dict:
    files, dirs = [], []
    if dirname.startswith('https://'):
        pass
    else:
        with os.scandir(dirname) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def read_file(path: str) -> str:
    with open(path) as fp:
        doc = fp.read()
    return doc


def load_template_file(file: str, category: str, fname: str) -> dict:
    tval = defaultdict(dict)
    tval['Metadata']['name'] = fname
    section = ''
    for ln, line in enumerate(file.splitlines(), start=1):
        if len(line):
            if m := re.match(r'^#\s+(.+)\s*$', line):
                if fname != m.group(1):
                    print(f'{ln:4} {fname} -- File name does not match heading {m.group(1)}')
            elif m := re.match(r'^##\s+(.+)\s*$', line):
                section = m.group(1)
                li1, li2 = '', ''
                if section not in ('Summary', 'Description', 'Metadata', 'Properties', 'Entries'):
                    print(f'{ln:4} {fname} -- Unknown section {section}')
                if section == 'Metadata':
                    tval[section] = {'name': fname}
                    cdefault = {'id': '${NAMESPACE_id}/' + fname, 'Instantiability': 'Concrete', 'Status': 'Stable'}
                    tval[section].update(cdefault if category == 'Classes' else {})
            elif m := re.match(r'^-\s+(.+)\s*$', line):
                li1 = m.group(1)
                if section in ('Metadata', 'Entries'):
                    k, v = li1.split(':', maxsplit=1)
                    tval[section].update({k.strip(): v.strip()})
                elif section == 'Properties':
                    pdefault = {'minCount': 0, 'maxCount': '*'} if category == 'Classes' else {}
                    tval[section].update({li1: pdefault})
            elif m := re.match(r'^\s+-\s+(.+)\s*$', line):
                li2 = m.group(1)
                if section == 'Properties':
                    if ':' in li2:
                        k, v = li2.split(':', maxsplit=1)
                        tval[section][li1].update({k.strip(): v.strip()})
                    else:
                        print(f'{ln:4} {fname} -- {section}?: {li1}: {li2}')
            elif section not in ('Description', 'Summary'):
                print(f'{ln:4} {fname} -- Unrecognized data?: {line}')
    missing = {'Classes': set(('Metadata', 'Properties')),
               'Properties': set(('Metadata',)),
               'Vocabularies': set(('Metadata', 'Entries'))}[category] - set(tval)
    if missing:
        print(f'     {fname} -- Missing required section {missing}')
    return dict(tval)


def dd():
    """
    Return a recursive defaultdict
    """
    return defaultdict(dd)


def load_template_from_list_dirs(rootdir: str) -> dict:
    """
    Load SPDX v3 template from individual files in markdown list format
    :param rootdir: top level in directory hierarchy
    """

    templ = dd()
    t1 = list_dir(rootdir)
    for f1 in t1['files']:
        print(f'     File {f1.path} ignored')
    for d1 in t1['dirs']:
        t2 = list_dir(d1.path)
        for f2 in t2['files']:
            print(f'     File {f2.path} ignored')
        for d2 in t2['dirs']:
            if d2.name not in MODEL_DIRS:
                raise ValueError(f'Unexpected Directory {d2.path}, not in {MODEL_DIRS}')
            t3 = list_dir(d2.path)
            for d3 in t3['dirs']:
                raise ValueError(f'Unexpected Directory at leaf {d3.path}')
            for f3 in t3['files']:
                if f3.name.startswith('_'):
                    print(f' Template {f3.path} ignored')
                else:
                    doc = read_file(f3.path)
                    fname = os.path.splitext(f3.name)[0]
                    templ[d1.name][d2.name][fname] = load_template_file(doc, d2.name, fname)
    return dict(templ)


def load_template_from_file(doc: str) -> dict:
    """
    Load SPDX v3 template in markdown table format
    :param doc: markdown file
    :return: 3-level template structure: Category / Instance / Values
        "Classes": [
          "class1": {
            "meta": {...}
            "Shape": {
              "head": [...]
              "body": [[...], [...]]
        "Properties": [
          "property1": {
            "meta": {...}
        "Vocabularies": [
          "vocabulary1": {
            "meta": {...}
            "entries": {...}
    """
    templ = {}
    l2, l3, l4 = '', '', ''
    for ln, line in enumerate(doc.splitlines(), start=1):
        if line:
            if line.startswith('#'):
                table_state = 0
                if m := re.match(r'^##(\s*)\d+\s+(.+?)\s*$', line):
                    l2 = m.group(2)
                    l3, l4 = '', ''
                    if l2 not in {'Classes', 'Properties', 'Vocabularies'}:
                        print(f'{ln:>6}: Unknown Category')
                elif m := re.match(r'^###(\s*)\d+\.\d+\s+(.+?)\s*$', line):
                    l3 = m.group(2)
                    l4 = ''
                elif m := re.match(r'^####(\s*)\d+\.\d+\.\d+\s+(.+?)\s*$', line):
                    l4 = m.group(2)
                elif m := re.match(r'^#(\s+)(.+?)\s*$', line):
                    pass    # title
                elif m := re.match(r'^##(\s+)(.+?)\s*$', line):
                    pass    # summary - must be last since categories are also at level 2
                else:
                    l4 = ''
                    print(f'{ln:>6}: Structure Error: {line}')
                if m and len(m.group(1)) == 0:
                    print(f'{ln:>6}: Warning: no space after heading level: {line}')
            elif l4 in {'Metadata', 'Shape', 'Vocabulary Entries'} and line.strip().startswith('|'):
                tl = [v.strip() for v in line.strip().strip('|').split('|')]
                if table_state == 0:
                    th = tl
                    table_state = 1
                elif table_state == 1:
                    if len(tl) == len(th):
                        templ[l2] = templ.get(l2, {})
                        templ[l2][l3] = templ[l2].get(l3, {})
                        if l4 in templ[l2][l3]:
                            print(f'{ln:>6}: Duplicate, overwriting {l2}/{l3}/{l4}')
                        templ[l2][l3][l4] = {'head': th, 'body': []}
                        table_state = 2
                    else:
                        print(f'{ln:>6}: Bad table header: {th}, {tl}')
                        table_state == -1
                elif table_state == 2:
                    if len(tl) == len(th):
                        templ[l2][l3][l4]['body'].append(tl)
                    else:
                        print(f'{ln:>6}: Bad table row: {th}, {tl}')
                        table_state == -1
    return templ


def atoi(s: str) -> int:
    i = 0
    if s:
        try:
            i = int(s)
        except ValueError:
            print(f'      converting invalid value "{s}" into 0')
    return i


def multopts(minc: str, maxc: str) -> list:
    if maxc:
        minc = atoi(minc)
        maxc = 0 if maxc == '*' else atoi(maxc)
    else:
        minc = maxc = atoi(minc)
    mo = {'minc': minc} if minc != 1 else {}
    mo.update({'maxc': maxc} if maxc != 1 else {})
    return jadn.opts_d2s(mo)


def fieldtype(typename: str) -> str:
    tmap = {
        'xsd:string': 'String',
        'xsd:integer': 'Integer',
        'xsd:decimal': 'Number',
        'xsd:dateTime': 'Timestamp'
    }
    return tmap[typename] if typename in tmap else typename


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')

    # Load data from directory tree of individual files
    # Local filesystem: TEMPLATE_ROOT_DIR
    # GitHub repo: TEMPLATE_ROOT_REPO

    tmp = load_template_from_list_dirs(TEMPLATE_ROOT_DIR)
    template = tmp['Core']

    # Convert all "Metadata" sections from Attribute-Value list to "meta" dict
    # for mc in template.values():
    #     for mt in mc.values():
    #         mt['meta'] = {ma[0]: ma[1] for ma in mt['Metadata']['body']}

    # Make up a Core namespace until the template defines it
    schema = {'info': {'package': 'http://www.example.com/foo'},
              'types': []}

    # Convert Class Properties (shape) sections to Record type definitions
    props = []
    for mt in template['Classes'].values():
        fields = []
        sect = mt.get('Properties', {})
        if not sect:
            print(f'Missing properties section - {mt["Metadata"]["name"]}')
        for fn, fv in enumerate(sect.items(), start=1):
            ftype = fv[1].get('type', '')
            if not ftype:
                print(f'Missing type - {mt["Metadata"]["name"]}:{fv[0]}')
            opts = multopts(fv[1]['minCount'], fv[1]['maxCount'])
            fields.append([fn, fv[0], fieldtype(ftype), opts, ''])
            props.append([fv[0], ftype, ''])
        schema['types'].append([mt['Metadata']['name'], 'Record', [], '', fields])

    # Validate redundant "Properties" files for consistency with Class properties
    for p in props:
        try:
            if template['Properties'][p[0]]['meta']['Range'] != p[1]:
                print(f'{str(p):40} != {template["Properties"][p[0]]["meta"]}')
        except KeyError:
            print(f'No Property {p[0]}')

    # Convert "Vocabularies" sections to Enumerated type definitions
    for mt in template['Vocabularies'].values():
        items = []
        sect = mt.get('Entries', {})
        if not sect:
            print(f'Missing entries section - {mt["Metadata"]["name"]}')
        for fn, fv in enumerate(sect.items(), start=1):
            items.append([fn, fv[0], fv[1]])
        schema['types'].append([mt['Metadata']['name'], 'Enumerated', [], '', items])

    # Generate information model (.jadn, .jidl) and JSON Schema (.json)
    # TODO: generate XML schema (.xsd), YAML, spreadsheet, Tag:Value, etc.
    outdir = os.path.join(DATA_DIR, OUTPUT_DIR)
    os.makedirs(outdir, exist_ok=True)
    jadn.dump(schema, os.path.join(outdir, OUTPUT_FILE + '.jadn'))
    jadn.convert.jidl_dump(schema, os.path.join(outdir, OUTPUT_FILE + '.jidl'))
    # jadn.translate.json_schema_dump(schema, os.path.join(outdir, OUTPUT_FILE + '.json'))

    # Check for completeness
    try:
        print('\n', '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
    except ValueError as e:
        print(f'\n{e}')
