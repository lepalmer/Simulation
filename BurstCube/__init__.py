import os

__version__ = "unknown"

try:
    from .version import get_git_version
    __version__ = get_git_version()
except Exception as message:
    print(message)

__author__ = "Jeremy Perkins"


try:
    os.environ['BURSTCUBE']
except KeyError:
    print("Warning: BURSTCUBE variable not set.")

