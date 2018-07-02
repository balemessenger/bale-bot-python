import setuptools

setuptools.setup(name='balebot',
                 version='1.1.3',
                 description='python framework for Bale messenger Bot API ',
                 author='bale',
                 author_email='balebot@elenoon.ir',
                 license='Apache-2.0',
                 install_requires=[
                     'aiohttp==2.3.7',
                     'asyncio==3.4.3',
                     'graypy==0.2.14',
                 ],
                 packages=setuptools.find_packages())
