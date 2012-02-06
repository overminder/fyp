import pip

class FailedToInstall(Exception):
    def __init__(self, exit_code, package_name):
        super(FailedToInstall, self).__init__(exit_code, package_name)
        self.exit_code = exit_code
        self.package_name = package_name

    def __repr__(self):
        return 'FailedToInstall: installation of %s returned %s' % (
                self.package_name, self.exit_code)

def install_package(package_name):
    exit_code = pip.main(['install', package_name, '--user'])
    if exit_code != 0:
        raise FailedToInstall(exit_code, package_name)

def uninstall_package(package_name):
    exit_code = pip.main(['uninstall', package_name, '-y'])

