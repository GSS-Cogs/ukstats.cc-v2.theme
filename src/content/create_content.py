import shutil
from configparser import ConfigParser
from pathlib import Path

# As this is eval'd, __file__ is actually instance/parts/instance/bin/interpreter
INSTANCE = Path(__file__).resolve().parent.parent.parent.parent
HERE = INSTANCE / 'src' / 'ukstats.ccv2.theme' / 'src' / 'content'

cp = ConfigParser()
cp.read(INSTANCE / 'buildout.cfg')

VAR_DIR = Path(cp['buildout']['var-dir'])

IMPORT_ROOT = VAR_DIR / 'instance' / 'import'
IMPORT_ROOT.mkdir(parents=True, exist_ok=True)

for f in IMPORT_ROOT.glob('*.zexp'):
    obj = f.stem
    if obj not in portal:
        portal.manage_importObject(f.name)
