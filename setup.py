import ast
import os
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('pylio/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as page:
    README = page.read()

setup(
    name='Pylio',
    version=VERSION,
    url='https://github.com/rekeninghub/pylio',
    license='MIT',
    author='Christoforus Surjoputro',
    author_email='cs_sanmar@yahoo.com',
    description='A python module to access https://helio.id email service.',
    long_description=README,
    packages=['pylio'],
    zip_safe=False,
    platforms='any',
    install_requires=['aiohttp']
    extras_require={
        'dev': ['nose'],
    },
    python_requires='~=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
