import jadn
import json
import os
import re
from collections import defaultdict
from urllib.request import urlopen, Request
from urllib.error import HTTPError

"""
Generate JADN information model and JSON serialization from SPDXv3 template files
"""

TEMPLATE_ROOT_DIR = os.path.join('..', 'spec-v3-template', 'model')
TEMPLATE_ROOT_REPO = 'https://api.github.com/repos/spdx/spec-v3-template/contents/model'
BASE = TEMPLATE_ROOT_REPO

OUTPUT_DIR = 'Out'
OUTPUT_FILE = 'spdxv3-from-list-template'
MODEL_DIRS = ('Classes', 'Properties', 'Vocabularies')
CATEGORY_METADATA = '.'
AUTH = {'Authorization': 'token ' + os.environ['GitHubToken']}      # GitHub public_repo personal access token


class WebDirEntry:
    """
    Fake os.DirEntry type for GitHub filesystem
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path


def dd():
    """
    Return a recursive defaultdict
    """
    return defaultdict(dd)


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


def list_dir(dirname: str) -> dict:
    """
    Return a dict listing the files and directories in a directory on local filesystem or GitHub repo.

    :param dirname: str - a filesystem path or GitHub API URL
    :return: dict {files: [DirEntry*], dirs: [DirEntry*]}
    Each list item is an os.DirEntry structure containing path and name attributes
    """
    files, dirs = [], []
    if dirname.startswith('https://'):
        with urlopen(Request(dirname, headers=AUTH)) as d:
            for dl in json.loads(d.read().decode()):
                url = 'url' if dl['type'] == 'dir' else 'download_url'
                entry = WebDirEntry(dl['name'], dl[url])
                (dirs if dl['type'] == 'dir' else files).append(entry)
    else:
        with os.scandir(dirname) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def read_file(path: str) -> str:
    if path.startswith('https://'):
        with urlopen(Request(path, headers=AUTH)) as fp:
            doc = fp.read().decode()
    else:
        with open(path) as fp:
            doc = fp.read()
    return doc


def scan_template_file(fpath: str, file: str, category: str, fname: str) -> dict:
    """
    Parse an SPDXv3 template markdown file into a structured object
    :param file: markdown content
    :param category: class type (one of "Classes, "Properties", "Vocabularies)
    :param fname: name of class
    :return: dict containing class properties
    """
    tval = defaultdict(dict)
    tval['Metadata']['name'] = fname
    section = ''
    for ln, line in enumerate(file.splitlines(), start=1):
        if len(line):
            if m := re.match(r'^#\s+(.+)\s*$', line):
                if fname != m.group(1):
                    print(f'  {fpath} line {ln} -- File name does not match heading {m.group(1)}')
            elif m := re.match(r'^##\s+(.+)\s*$', line):
                section = m.group(1)
                li1, li2 = '', ''
                if section not in ('Summary', 'Description', 'Metadata', 'Properties', 'Entries'):
                    print(f'  {fpath} line {ln} -- Unknown section: "{section}"')
                if section == 'Metadata':
                    tval[section] = {'name': fname}
                    # default property values from top-level "Defaults.md"
                    cdefault = {'id': '${NAMESPACE_id}/' + fname, 'Instantiability': 'Concrete', 'Status': 'Stable'}
                    tval[section].update(cdefault if category == 'Classes' else {})
            elif m := re.match(r'^[-*]\s+(.+)\s*$', line):
                li1 = m.group(1)
                if section in ('Metadata', 'Entries'):
                    k, v = li1.split(':', maxsplit=1)
                    tval[section].update({k.strip(): v.strip()})
                elif section == 'Properties':
                    pdefault = {'minCount': 0, 'maxCount': '*'} if category == 'Classes' else {}
                    tval[section].update({li1: pdefault})
            elif m := re.match(r'^\s+[-*]\s+(.+)\s*$', line):
                li2 = m.group(1)
                if section == 'Properties':
                    if ':' in li2:
                        k, v = li2.split(':', maxsplit=1)
                        tval[section][li1].update({k.strip(): v.strip()})
                    else:
                        print(f'  {fpath} line {ln} {section}/{li1} -- bad data: "{li2}"')
            elif section not in ('Description', 'Summary'):
                print(f'  {fpath} line {ln} -- Unrecognized data: "{line}"')
    missing = {CATEGORY_METADATA: set(('Metadata',)),
               'Classes': set(('Metadata', 'Properties')),
               'Properties': set(('Metadata',)),
               'Vocabularies': set(('Metadata', 'Entries'))}[category] - set(tval)
    if missing:
        print(f'  {fpath} -- Missing required section: {missing}')
    return dict(tval)


def load_template_from_list_dirs(rootdir: str) -> dict:
    """
    Load SPDX v3 template from individual files in markdown list format
    :param rootdir: top level in directory hierarchy
    """

    def _f(path: str) -> str:
        return path.removeprefix(BASE)

    templ = dd()
    t1 = list_dir(rootdir)
    for f1 in t1['files']:
        print(f'  {_f(f1.path)} -- file at root level ignored')
    for d1 in t1['dirs']:
        t2 = list_dir(d1.path)
        for f2 in t2['files']:
            doc = read_file(f2.path)
            fname = os.path.splitext(f2.name)[0]
            templ[d1.name][CATEGORY_METADATA][fname] = scan_template_file(_f(f2.path), doc, CATEGORY_METADATA, fname)
        for d2 in t2['dirs']:
            if d2.name not in MODEL_DIRS:
                raise ValueError(f'{_f(d2.path)} -- unexpected directory, not in {MODEL_DIRS}')
            t3 = list_dir(d2.path)
            for d3 in t3['dirs']:
                raise ValueError(f'{_f(d3.path)} -- unexpected directory at leaf level')
            for f3 in t3['files']:
                if f3.name.startswith('_'):
                    print(f'  {_f(f3.path)} -- _filename ignored')
                else:
                    doc = read_file(f3.path)
                    fname = os.path.splitext(f3.name)[0]
                    templ[d1.name][d2.name][fname] = scan_template_file(_f(f3.path), doc, d2.name, fname)
    return dict(templ)


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')

    # Load data from directory tree of individual files
    print(f'Scanning template files from "{BASE}"')
    templates = load_template_from_list_dirs(BASE)

    print(f'\nConverting class model to information model in directory "{OUTPUT_DIR}"')
    for package, template in templates.items():
        if package != 'Core':
            continue            # Ignore other packages until template has real data

        try:
            namespace = template[CATEGORY_METADATA][package]['Metadata']['id']
        except KeyError:
            namespace = 'http://foo.com/' + package
        schema = {'info': {'package': namespace}, 'types': []}

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
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        jadn.dump(schema, os.path.join(OUTPUT_DIR, OUTPUT_FILE + '.jadn'))
        jadn.convert.jidl_dump(schema, os.path.join(OUTPUT_DIR, OUTPUT_FILE + '.jidl'))
        jadn.translate.json_schema_dump(schema, os.path.join(OUTPUT_DIR, OUTPUT_FILE + '.json'))

        # Check for completeness
        try:
            print('\n', '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
        except ValueError as e:
            print(f'\n{e}')
