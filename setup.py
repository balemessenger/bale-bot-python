import setuptools

with open('CHANGELOG.md', mode='rt', encoding='utf-8') as f:
    long_description = f.read()

requires = [
        'aiohttp==2.3.7',
        'asyncio==3.4.3',
        'graypy==0.2.14',
        'backoff==1.6.0',
        'pillow==5.2.0',
        ]

setuptools.setup(name='balebot',
                 version='1.2.8',
                 description='python framework for Bale messenger Bot API',
                 author='bale',
                 author_email='balebot@elenoon.ir',
                 license='GNU',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/balemessenger/bale-bot-python',
                 install_requires=requires,
                 packages=setuptools.find_packages())
