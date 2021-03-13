from setuptools import setup, find_packages

setup(
    name='git-plan',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'dependency_injector[yaml]',
        'cachetools',
        'rich',
        'inquirer',
        'click',
        'version-query'
    ]
)
