from setuptools import setup, find_packages

setup(
        name             = 'libcbm_runner',
        version          = '0.1.1',
        description      = 'libcbm_runner is a python package for running carbon budget simulations.',
        long_description = open('README.md').read(),
        license          = 'MIT',
        url              = 'https://github.com/xapple/libcbm_runner',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        packages         = find_packages(),
        install_requires = ['autopaths', 'plumbing', 'pymarktex', 'pandas', 'pystache',
                            'simplejson', 'matplotlib', 'tqdm'],
    )
