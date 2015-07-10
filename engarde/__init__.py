__version__ = '0.2.0'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
