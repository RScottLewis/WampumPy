#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Wampum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['wampum.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/wampum.png'])
    ]

setup(
    name="Wampum",
    version=version.WAMPUM_VERSION,
    install_requires=[
        'pyaes>=0.1a1',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'protobuf',
        'dnspython',
        'jsonrpclib-pelix',
        'PySocks>=1.6.6',
    ],
    packages=[
        'wampum',
        'wampum_gui',
        'wampum_gui.qt',
        'wampum_plugins',
        'wampum_plugins.audio_modem',
        'wampum_plugins.cosigner_pool',
        'wampum_plugins.email_requests',
        'wampum_plugins.greenaddress_instant',
        'wampum_plugins.hw_wallet',
        'wampum_plugins.keepkey',
        'wampum_plugins.labels',
        'wampum_plugins.ledger',
        'wampum_plugins.trezor',
        'wampum_plugins.digitalbitbox',
        'wampum_plugins.trustedcoin',
        'wampum_plugins.virtualkeyboard',
    ],
    package_dir={
        'wampum': 'lib',
        'wampum_gui': 'gui',
        'wampum_plugins': 'plugins',
    },
    package_data={
        'wampum': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/wampum.mo',
        ]
    },
    scripts=['wampum'],
    data_files=data_files,
    description="Lightweight Bitcoin Wallet",
    author="Scott Lewis",
    author_email="sales@greenspacepros.com",
    license="ITM Licence",
    url="https://wampum.org",
    long_description="""Lightweight Bitcoin Wallet"""
)
