from setuptools import setup

setup(
    name='rgscraper',
    version='0.1',
    py_modules=[
        'configs',
        'rgscraper',
        'parsers',
        'transformers'
    ],
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
        rgscraper=rgscraper:get_proj_stats
    ''',
)