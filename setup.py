from setuptools import setup, find_packages
setup(
    name = 'diceroll',
    version = '0.1',
    packages = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    py_modules=['diceroll'],
    test_suite = 'tests',
    tests_require = ['mock'],
)