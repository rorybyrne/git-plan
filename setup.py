from setuptools import find_packages, setup

setup(
    name='git-plan',
    use_scm_version=True,
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=[
        'dependency_injector[yaml]',
        'cachetools',
        'rich',
        'inquirer',
        'humanize'
    ]
)
