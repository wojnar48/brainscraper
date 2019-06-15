from setuptools import setup

setup(
    name='rotoscrape',
    version='0.1',
    py_modules=['rotoscrape'],
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4',
        'MLB-StatsAPI',
        'ipython',
        'ipdb',
        'selenium==3.141.0',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        rotoscrape=rotoscrape:get_stats
    ''',
)