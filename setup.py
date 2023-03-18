from setuptools import setup
from setuptools.command.sdist import sdist as _sdist
import subprocess

VERSION = '1.0.0'

class sdist(_sdist):
    def run(self):
        subprocess.call(['tar', '-cJf', 'dist/hashfile_{}.orig.tar.xz'.format(VERSION), '--exclude-vcs', '--exclude', 'dist', '.'])
        _sdist.run(self)

setup(
    name='hashfile',
    version=VERSION,
    description='File hash calculator',
    author='Juan Martin',
    author_email='juanmartincas@gmail.com',
    url='',
    cmdclass={'sdist': sdist},
    install_requires=[
        'aiofiles',
        'argparse',
        'configparser',
        'dbus-python',
        'PyGObject',
    ],
    entry_points={
        'console_scripts': [
            'hashfile = hashfile:main',
        ]
    }
)
