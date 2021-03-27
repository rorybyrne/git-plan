<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/110315084-a7e39f80-8000-11eb-8a14-3799c7e2cfd3.png">
</p>
<p align="center">
  <b>A better workflow for git.</b>
</p>
<hr></hr>
<p align="center">
  <img src="https://github.com/synek/git-plan/workflows/Full%20Tests/badge.svg">
</p>

Git plan allows you to write your commit messages in-advance, before you start coding. Then you can use those planned-commits as a template for your commit message when you are ready to commit your work. This makes it easier to plan your work and stay on-track.

This tool is in *alpha* stage. If anything breaks, please open an issue.

## Installation

`git plan` is not yet available for general installation. To install it from source (i.e. for development), see the development installation instructions below.

## Usage
To use the tool, run `git plan init` (or simply `gp <command>`) to initialize, and then `git plan add` to plan a new commit. When you are ready to make a `commit` to git, use `git plan commit` to use the plan as a template for your commit message.

* `git plan init` - initialize git plan in the `.plan/` directory
* `git plan` - create a new plan, or list existing plans
* `git plan --version` - print version info
* `git plan --help` - print help
* `git plan list [-l/--long] [-a/--all]` - list existing plans
* `git plan add` - plan a new commit
* `git plan edit` - edit an existing plan
* `git plan delete` - delete a plan
* `git plan commit` - commit your work, choosing a plan as your commit message template

## Contributing

* Download the tool and try it out
* Create an [issue](https://github.com/synek/git-plan/issues) if you find a bug
* Open a [discussion topic](https://github.com/synek/git-plan/discussions) if you have a suggestion or question
* [Fork](https://guides.github.com/activities/forking/) the repository, fix a bug or add a feature, and open a PR
* If you'd like making a contribution please ask and we can help you.

### Development

* Clone: `git clone https://github.com/synek/git-plan && cd git-plan`
* Optionally create a virtualenv: `python -m venv .venv && source .venv/bin/activate`
* Install: `poetry install`
* Check: `git plan --version` or `gp --version`
* Run tests: `tox`
* Install pre-commit hooks: `poetry run pre-commit install`

You the minimum support Python version is `3.8` but there is an [open issue](https://github.com/synek/git-plan/issues/73) to support `3.6`.

### Pre-Commit hooks

Failure on any of the hooks will prevent the action taking place.

* [pylint](https://pylint.org/) on changed source files
* [mypy](http://mypy-lang.org/) on changed source files
* [tox](https://tox.readthedocs.io/en/latest/) test suite runs

## Background
Here is an interesting [blog post]("https://arialdomartini.wordpress.com/2012/09/03/pre-emptive-commit-comments/) about pre-emptive commit comments.
