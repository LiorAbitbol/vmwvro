from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vmwvro',
    version='1.0.2b1',
    description='A simple api library to interface with VMware vRealize Orchestrator (vRO).',
    long_description=long_description,
    url='https://pypi.python.org/pypi/vmwvro',
    author='Lior P. Abitbol',
    author_email='liorabitbol@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
        'Programming Language :: Python :: 3.5'
    ],
    keywords='vmware vro orchestrator api development',
    packages=['vmwvro'],
    include_package_data=True,
    package_data={'': ['LICENSE.txt', 'requirements.txt']},
    install_requires=['requests'],
    zip_safe=False
)
