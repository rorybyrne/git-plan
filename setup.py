from setuptools import setup, find_packages

setup(
    name='git-plan',
    use_scm_version=True,
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    install_requires=[
        'dependency_injector[yaml]',
        'cachetools',
        'rich',
        'inquirer'
    ]
)
