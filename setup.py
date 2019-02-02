from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='test_1c',
    version='0.26',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={'console_scripts':['test_1c = test_1c.main:main']},
    include_package_data=True,
    install_requires=[
        'selenium==3.141.0',
        'Pillow==5.3.0',
        'pywin32==223'
        ],
    license='',
    author="Kuznetsov Gregory",
    author_email="a925041@yandex.ru",
    url = 'https://github.com/nemo0101/1C-Retail-smoke-tests',
)
