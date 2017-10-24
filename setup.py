from setuptools import setup, find_packages

setup(
	name='trans',
	version='1.0.0',
	author='Nyloner',
	author_email='nyloner.root@gmail.com',
    url='https://github.com/Nyloner',
	description='A simple tool for translation.',
	license='BSD',
	packages=find_packages(),
	install_requires=['requests', 'bs4', 'lxml']
);
