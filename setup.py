from setuptools import setup, find_packages

setup(
    name='git-plan',
    use_scm_version=True,
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools_scm'],
    package_data={'': ['git_plan/_version']},
    include_package_data=True,
    install_requires=[
        'dependency_injector[yaml]',
        'cachetools',
        'rich',
        'inquirer'
    ]
)
