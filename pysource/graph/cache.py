
import os
import json
import atexit
failure_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        './cache/failures.json')

try:
    with open(failure_file) as f:
        known_failures = set(json.load(f))
except IOError:
    with open(failure_file, 'w') as f:
        known_failures = set(['_winreg', 'msilib', 'win32con', 'win32api',
                '_subprocess', 'msvcrt', 'EasyDialogs',
                'rourl2path', '_scproxy',
                '_sha', '_sha512', '_md5', '_sha256', 'win32evtlog',
                'win32evtlogutil', '_xmlrpclib', 'builtins', 'debug'])
        json.dump(list(known_failures), f)

def shall_fail(name):
    return name in known_failures or name.startswith('win32')

@atexit.register
def write_back():
    with open(failure_file, 'w') as f:
        json.dump(list(known_failures), f)

