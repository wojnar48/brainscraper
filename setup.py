from setuptools import setup

setup(
    name='rotoscrape',
    version='0.1',
    py_modules=['rotoscrape'],
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4'
    ],
    entry_points='''
        [console_scripts]
        rotoscrape=rotoscrape:get_rotowire_data
    ''',
)