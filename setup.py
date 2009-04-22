from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-googleanalytics",
    version = "1.0",
    url = 'http://github.com/clintecker/python-googleanalytics',
    license = 'BSD',
    description = "A python library for talking to the Google Analytics API",
    long_description = read('README.md'),
    
    author = 'Clint Ecker',
    author_email = 'me@clintecker.com',
    
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    
    install_requires = ['setuptools',],
    
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
    ]
)