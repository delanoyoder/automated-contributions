from os.path import dirname, abspath
from os import environ

BaseDir = f"{environ.get('VIRTUAL_ENV')}/.."
SrcDir = dirname(abspath(__file__))
ConfigsDir = f"{BaseDir}/configs"
