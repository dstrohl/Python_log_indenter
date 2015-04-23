from setuptools import setup

setup(
    name='python_log_indenter',
    version='0.9',
    packages=['python_log_indenter', 'python_log_indenter.tests'],
    url='http://python-log-indenter.readthedocs.org/en/latest/',
    license='GPLv2',
    author='Dan Strohl',
    author_email='dan@wjcg.net',
    description='A python LoggerAdapter class that provides automatic indenting for logging.',
    tests_require=['testfixtures'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Logging'
    ],
    keywords='log LogAdapter indent logger logging extension plugin helper Logger readable'

)
