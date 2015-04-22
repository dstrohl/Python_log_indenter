from distutils.core import setup

setup(
    name='python_log_indenter',
    version='0.9',
    packages=['python_log_indenter', 'python_log_indenter.tests'],
    url='http://python-log-indenter.readthedocs.org/en/latest/',
    license='GPL2',
    author='Dan Strohl',
    author_email='dan@wjcg.net',
    description='',
    extras_require=dict(
        test=['testfixtures'],
        )
)
