"""
Translate each schema file in Source directory to multiple formats in Out directory
"""
import jadn
import os

SCHEMA_DIR = 'Schemas'
DATA_DIR = 'Data3'


def load_any(path: str) -> dict:
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