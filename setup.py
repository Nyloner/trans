from setuptools import setup, find_packages

setup(
    name='trans',
    version='1.0.0',
    author='Nyloner',
    author_email='nyloner.root@gmail.com',
    url='https://github.com/Nyloner/trans',
   	description='A Simple Translation Tool In Your Command Line.',
   	license='BSD',
   	packages=find_packages(),
   	install_requires=['requests', 'bs4', 'lxml','termcolor'],
   	entry_points={
            'console_scripts': [
                'trans = trans.trans:execute'
            ]
        }
);
