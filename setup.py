from setuptools import setup, find_packages


setup(
    name='smartertodo',
    version='1.0.2',
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
