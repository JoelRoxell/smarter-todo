from setuptools import setup, find_packages


setup(
    name='smartertodo',
    version='',
    install_requires=[
        'requests',
        'tabulate'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'smartertodo = smartertodo.cli:run'
        ]
    }
)
