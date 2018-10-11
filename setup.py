from setuptools import setup, find_packages
import os 

here = os.path.abspath(os.path.dirname(__file__))

requires = [
        'aiohttp==2.3.7',
        'asyncio==3.4.3',
        'graypy==0.2.14',
        'backoff==1.6.0',
        'pillow==5.2.0',
        ]

with open('README.md', mode='rt', encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(os.path.join(here, 'balebot', '__version__.py'), mode='rt', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
        name=about['__title__'],
        version=about['__version__'],
        description=about['__description__'],
        author=about['__author__'],
        author_email=about['__author_email__'],
        license=about['__license__'],
        long_description=long_description,
        long_description_content_type='text/markdown',
        url=about['__url__'],
        install_requires=requires,
        packages=find_packages(),
)
