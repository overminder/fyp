import pdb
from pysource.log import get_logger

logger = get_logger('pysource.graph.installer')

known_failures = set(['_winreg', 'msilib', 'win32con', 'win32api',
        '_subprocess', 'msvcrt', 'EasyDialogs', 'rourl2path', '_scproxy',
        '_sha', '_sha512', '_md5', '_sha256', 'win32evtlog',
        'win32evtlogutil', '_xmlrpclib'])

def shall_fail(name):
    return name in known_failures or name.startswith('win32')

class FailedToInstall(Exception):
    def __init__(self, reason, package_name):
        super(FailedToInstall, self).__init__(reason, package_name)
        self.reason = reason
        self.package_name = package_name

    def __repr__(self):
        return 'FailedToInstall: installation of %s failed. reason: %s' % (
                self.package_name, self.reason)

def install_package(package_name):
    pip_install(package_name)

def uninstall_package(package_name):
    pip_uninstall(package_name)

# Internal: pip hacking.
from pip.basecommand import load_all_commands, command_dict
from pip.exceptions import InstallationError

def initialize_pip_commands():
    load_all_commands()
    return command_dict['install'], command_dict['uninstall']

pip_installer, pip_uninstaller = initialize_pip_commands()

def pip_install(package_name):
    if shall_fail(package_name):
        raise FailedToInstall('not available', package_name)

    logger.warn('installing %s' % package_name)
    opt, args = pip_installer.parser.parse_args([package_name, '--user'])
    try:
        pip_installer.run(opt, args)
    except InstallationError as e:
        logger.warn('installation of %s failed. reason: %s' % (
            package_name, str(e)))
        raise FailedToInstall(str(e), package_name)

def pip_uninstall(package_name):
    opt, args = pip_uninstaller.parser.parse_args([package_name, '-y'])
    pip_uninstaller.run(opt, args)

