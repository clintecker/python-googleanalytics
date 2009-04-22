from setuptools import setup, find_packages

setup(
    name = "python-googleanalytics",
    version = "1.0",
    url = 'http://github.com/clintecker/python-googleanalytics',
    license = 'BSD',
    description = "A python library for talking to the Google Analytics API",
    author = 'Clint Ecker',
    packages=['googleanalytics'],
    package_dir={'': 'src'},
    install_requires = ['setuptools',],
)