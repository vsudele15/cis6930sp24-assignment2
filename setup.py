from setuptools import setup, find_packages

setup(
	name='assignment2',
	version='1.0',
	author='Vaidehi Sudele',
	authour_email='vsudele@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)