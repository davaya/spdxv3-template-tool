import jadn
import os
import re

"""
Generate serializations from an SPDX v3 template using a JADN information model

Template is currently a single markdown file, but a collection of individual GitHub files
in a simplified format is proposed.
"""

DATA_DIR = 'Templates'
OUTPUT_DIR = 'Out'
TEMPLATE_FILE = 'SpdxV3 Core Namespace Template.md'
OUTPUT_FILE = 'spdxv3-from-template'


def load_template(doc: str) -> dict:
    """
    Load SPDX v3 template in markdown format
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
        'xsd:decimal': 'Number'
    }
    return tmap[typename] if typename in tmap else typename


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')

    # Load data from single template file, or collect from individual class files on GitHub
    with open(os.path.join(DATA_DIR, TEMPLATE_FILE), 'r') as fp:
        template = load_template(fp.read())

    # Convert all "Metadata" sections from Attribute-Value list to "meta" dict
    for mc in template.values():
        for mt in mc.values():
            mt['meta'] = {ma[0]: ma[1] for ma in mt['Metadata']['body']}

    # Make up a Core namespace until the template defines it
    schema = {'info': {'package': 'http://www.example.com/foo'},
              'types': []}

    # Convert "Shape" sections to Record type definitions
    props = []
    for mt in template['Classes'].values():
        cx = {v: n for n, v in enumerate(mt['Shape']['head'])}
        fields = []
        for fn, fv in enumerate(mt['Shape']['body'], start=1):
            opts = multopts(fv[cx['Min Count']], fv[cx['Max Count']])
            fields.append([fn, fv[cx['Property']], fieldtype(fv[cx['Datatype']]), opts, fv[cx['Format']]])
            props.append([fv[cx['Property']], fv[cx['Datatype']], fv[cx['Format']]])
        schema['types'].append([mt['meta']['name'], 'Record', [], '', fields])

    # Validate "Properties" for consistency with Shapes
    for p in props:
        try:
            if template['Properties'][p[0]]['meta']['Range'] != p[1]:
                print(f'{str(p):40} != {template["Properties"][p[0]]["meta"]}')
        except KeyError:
            print(f'No Property {p[0]}')

    # Convert "Vocabularies" sections to Enumerated type definitions
    for mt in template['Vocabularies'].values():
        cx = {v: n for n, v in enumerate(mt['Vocabulary Entries']['head'])}
        items = []
        for fn, fv in enumerate(mt['Vocabulary Entries']['body'], start=1):
            items.append([fn, fv[cx['Entry Value']], fv[cx['Entry Description']]])
        schema['types'].append([mt['meta']['name'], 'Enumerated', [], '', items])

    # Generate information model (.jadn, .jidl) and JSON Schema (.json)
    # TODO: generate XML schema (.xsd), YAML, spreadsheet, Tag:Value, etc.
    outdir = os.path.join(DATA_DIR, OUTPUT_DIR)
    os.makedirs(outdir, exist_ok=True)
    jadn.dump(schema, os.path.join(outdir, OUTPUT_FILE + '.jadn'))
    jadn.convert.jidl_dump(schema, os.path.join(outdir, OUTPUT_FILE + '.jidl'))
    jadn.translate.json_schema_dump(schema, os.path.join(outdir, OUTPUT_FILE + '.json'))

    # Check for completeness
    print('\n', '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
